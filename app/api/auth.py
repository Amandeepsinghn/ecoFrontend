from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.user import (UserCreate, UserResponse, UserLogin, TokenResponse)
from app.core.jwt import create_access_token
from app.services.user_service import create_user, authenticate_user
from app.api.deps import get_db, get_current_user
from app.db.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register",response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.post("/login", response_model = TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)): 

    user = authenticate_user(db, user_data.email, user_data.password)

    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer","role": "admin" if user.is_admin else "customer"}





    