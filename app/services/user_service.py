from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends

from app.core.security import hash_password,verify_password
from app.db.models import User
from app.schemas.user import UserCreate
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

def get_all_products(db:Session) -> list[Product]:
    return db.query(Product).order_by(Product.id).all()                                                        

def get_product_by_id(product_id: int, db: Session)-> Product:
    return db.query(Product).filter(product_id == Product.id).first()


