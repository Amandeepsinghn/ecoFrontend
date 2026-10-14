
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Order, Product, Order_Item
from app.schemas.order import OrderCreate


def create_order(
    db: Session,
    user_id: int,
    order_data: OrderCreate
) -> Order:
    try:

        product_ids = [item.product_id for item in order_data.items]

        if len(product_ids) != len(set(product_ids)):
            raise HTTPException(
                status_code=400,
                detail="A product can only appear once per order"
            )


        products = {}

        for item in order_data.items:
            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found"
                )

            if product.stock is None or product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {product.name}"
                )

            products[item.product_id] = product


        total_price = sum(
            products[item.product_id].price * item.quantity
            for item in order_data.items
        )


        order = Order(
            user_id=user_id,
            total_price=total_price,
            status="pending"
        )

        db.add(order)
        db.flush()


        for item in order_data.items:
            product = products[item.product_id]

            order_item = Order_Item(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price
            )

            db.add(order_item)
            product.stock -= item.quantity


        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise