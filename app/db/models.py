from sqlalchemy import Integer, Float, Column, String, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    user_name = Column(String, nullable = False)

    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = True)

    credit = Column(Integer, default=1000, nullable= True)
    is_admin = Column(Boolean, default=False, nullable=False)

    products = relationship("Product", back_populates ="owner")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    price = Column(Float, nullable = False)
    stock = Column(Integer)
    description = Column(String, nullable = True)
    product_type = Column(String, nullable= True)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates = "products")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True,)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable= False)
    status = Column(String, nullable= False, default="pending")

    customer = relationship("User")
    items = relationship("Order_Item", back_populates="order", cascade = "all,delete-orphan")

class Order_Item(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable= False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable= False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")



