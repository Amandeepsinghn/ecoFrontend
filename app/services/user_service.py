from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, Depends

from app.core.security import hash_password,verify_password
from app.db.models import User
from app.schemas.user import UserCreate, ProfileUpdate
from app.db.models import Product



def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")
    
    user = User(
        user_name=user_data.user_name,
        email=user_data.email,
        password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db:Session, email:str, password: str) -> User:
    user = (db.query(User).filter(User.email ==email).first())
    
    if not user:
        raise HTTPException(status_code=401, detail = "Invalid email or password")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code = 401, detail = "Invalid email or password")

    return user

def update_profile(db: Session, user_id: int, profile_data: ProfileUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    changing_password = (
        profile_data.current_password is not None
        or profile_data.new_password is not None
    )
    if changing_password:
        if not profile_data.current_password or not profile_data.new_password:
            raise HTTPException(
                status_code=400,
                detail="Current password and new password are both required",
            )
        if not verify_password(profile_data.current_password, user.password):
            raise HTTPException(status_code=401, detail="Current password is incorrect")
        user.password = hash_password(profile_data.new_password)

    if profile_data.email is not None and profile_data.email != user.email:
        taken = db.query(User).filter(User.email == profile_data.email).first()
        if taken:
            raise HTTPException(status_code=409, detail="Email already registered")
        user.email = profile_data.email

    if profile_data.user_name is not None:
        user.user_name = profile_data.user_name

    db.commit()
    db.refresh(user)
    return user

def get_all_products(db:Session) -> list[Product]:
    return (
        db.query(Product)
        .options(selectinload(Product.photos))
        .order_by(Product.id)
        .all()
    )

def get_product_by_id(db: Session, product_id: int) -> Product:
    product = (
        db.query(Product)
        .options(selectinload(Product.photos))
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


