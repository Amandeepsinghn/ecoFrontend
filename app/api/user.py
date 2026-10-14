from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session

from db.models import User
from app.api.deps import get_db, get_current_user
from services import user_service


router = APIRouter(prefix="/users", tags=["User"])

@router.get("/products")
def get_all_products(db: Session = Depends(get_db), current_user: User = get_current_user()):
    return user_service.get_all_products()

@router.get("/products/{product_id}")
def get_product_id(product_id: int, db: Session = Depends(get_db), current_user: User = get_current_user()):
    return user_service.get_product_by_id(db, product_id)