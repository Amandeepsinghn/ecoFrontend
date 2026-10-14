
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_admin
from app.db.models import User
from app.schemas.admin.response import AdminUserResponse,AdminProductCreateReasponse
from app.schemas.admin.request import AdminRoleUpdate,AdminProductCreate,AdminProductUpdate,AdminStockUpdate
from app.services import admin_services

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.patch("/users/{user_id}/role", response_model=AdminUserResponse)
def update_user_role(user_id: int, role_data: AdminRoleUpdate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin),):
    
    if user_id == admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot change your own admin role",
        )
    return update_user_admin_status(db, user_id, role_data.is_admin)

@router.post("/products", response_model=AdminProductCreateReasponse, status_code=201)
def create_product(product_data: AdminProductCreate, db:Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return admin_services.create_product(db, product_data)

@router.get("/products", response_model=list[AdminProductCreateReasponse])
def get_all_products(db:Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return admin_services.get_all_products(db)

@router.get("/products/{product_id}", response_model=AdminProductCreateReasponse)
def get_product(product_id : int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return admin_services.get_product_by_id(db, product_id)

@router.patch("/products/{product_id}", response_model=AdminProductCreateReasponse)
def update_product(product_id: int, product_data: AdminProductUpdate,db: Session = Depends(get_db), current_admin: User= Depends(get_current_admin)):
    return admin_services.AdminProductUpdate(db, product_id, product_data)

@router.patch("/products/{product_id}/stock", response_model= AdminProductCreateReasponse)
def update_stock(product_id: int, stock_data: AdminStockUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return admin_services.update_product_stock(db, product_id, stock_data.stock)

@router.delete("/products,{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    admin_services.delete_product(db, product_id)




