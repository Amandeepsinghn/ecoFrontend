from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.api.deps import get_db, get_current_user
from app.schemas.admin.response import AdminProductCreateReasponse
from app.schemas.user import UserProfile, ProfileUpdate
from app.services import user_service


router = APIRouter(prefix="/users", tags=["User"])

@router.get("/profile", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/profile", response_model=UserProfile)
def update_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_profile(db, current_user.id, profile_data)

@router.get("/products", response_model=list[AdminProductCreateReasponse])
def get_all_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.get_all_products(db)

@router.get("/products/{product_id}", response_model=AdminProductCreateReasponse)
def get_product_id(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.get_product_by_id(db, product_id)
