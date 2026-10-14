from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user,get_db
from app.db.models import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_services import create_order

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse, status_code=201)
def checkout(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return create_order(
        db=db,
        user_id=current_user.id,
        order_data=order_data
    )