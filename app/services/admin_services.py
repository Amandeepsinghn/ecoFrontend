from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models import User,Product
from app.schemas.admin.request import AdminProductCreate,AdminStockUpdate,AdminProductUpdate


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

def create_product(db:Session, product_data: AdminProductCreate) -> Product:
    product = Product(name= product_data.name, 
                      price = product_data.price, 
                      stock = product_data.price, 
                      description= product_data.description,
                      product_type= product_data.product_type
                    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_all_products(db:Session)-> list[Product]:
    return db.query(Product).order_by(Product.id).all()

def get_product_by_id(db:Session,product_id : int)-> Product:
    product = (db.query(Product).filter(Product.id == product_id).first())

    if product is None:
        raise HTTPException(status_code=404 ,details = "Product not found")
    
    return product

def update_product(db:Session, product_id: int, product_data: AdminProductCreate) -> Product:
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

    db.delete(product)
    db.commit()











