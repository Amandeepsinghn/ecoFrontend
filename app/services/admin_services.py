from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, UploadFile

from app.core.images import delete_image, upload_image
from app.db.models import User, Product, ProductPhoto
from app.schemas.admin.request import AdminProductCreate, AdminStockUpdate, AdminProductUpdate


def get_all_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id).all()

def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def update_admin_status(db: Session, user_id: int, is_admin: bool)-> User:
    user = get_user_by_id(db,user_id)
    user.is_admin = is_admin

    db.commit()
    db.refresh(user)
    return user

def delete_user_admin(db:Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)

    db.delete(user)
    db.commit()

def create_product(
    db: Session,
    product_data: AdminProductCreate,
    user_id: int,
    files: list[UploadFile] | None = None,
) -> Product:
    product = Product(name= product_data.name, 
                      price = product_data.price, 
                      stock = product_data.stock, 
                      description= product_data.description,
                      product_type= product_data.product_type,
                      user_id= user_id,
                    )
    db.add(product)
    db.commit()
    db.refresh(product)

    if files:
        return add_product_photos(db, product.id, files)

    return get_product_by_id(db, product.id)

def get_all_products(db:Session)-> list[Product]:
    return (
        db.query(Product)
        .options(selectinload(Product.photos))
        .order_by(Product.id)
        .all()
    )

def get_product_by_id(db:Session,product_id : int)-> Product:
    product = (
        db.query(Product)
        .options(selectinload(Product.photos))
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

def update_product(db:Session, product_id: int, product_data: AdminProductUpdate) -> Product:
    product = get_product_by_id(db, product_id)

    updates = product_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

def update_product_stock(db:Session, product_id: int, stock: int) -> Product:
    product = get_product_by_id(db, product_id)

    product.stock = stock

    db.commit()
    db.refresh(product)

    return product

def delete_product(db:Session, product_id : int)-> None:
    product = get_product_by_id(db, product_id)
    public_ids = [photo.public_id for photo in product.photos]

    db.delete(product)
    db.commit()

    for public_id in public_ids:
        delete_image(public_id)


def add_product_photos(db: Session, product_id: int, files: list[UploadFile]) -> Product:
    product = get_product_by_id(db, product_id)

    if not files:
        raise HTTPException(status_code=400, detail="At least one photo is required")

    saved_public_ids = []
    try:
        for file in files:
            url, public_id = upload_image(file)
            saved_public_ids.append(public_id)
            db.add(ProductPhoto(product_id=product.id, url=url, public_id=public_id))
        db.commit()
    except HTTPException:
        db.rollback()
        for public_id in saved_public_ids:
            delete_image(public_id)
        raise
    except Exception:
        db.rollback()
        for public_id in saved_public_ids:
            delete_image(public_id)
        raise HTTPException(status_code=502, detail="Photo upload failed")

    db.expire_all()
    return get_product_by_id(db, product.id)


def delete_product_photo(db: Session, product_id: int, photo_id: int) -> None:
    product = get_product_by_id(db, product_id)
    photo = next((item for item in product.photos if item.id == photo_id), None)

    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    public_id = photo.public_id
    db.delete(photo)
    db.commit()
    delete_image(public_id)











