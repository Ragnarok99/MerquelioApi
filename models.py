from datetime import datetime
from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class ShoppingCart(Base):
    __tablename__ = 'shoppingCarts'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    created_at = Column(Date)
    products = relationship("Product", back_populates="cart")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)
    cart_id = Column(Integer, ForeignKey("shoppingCarts.id"))
    # price = Column(String, default=0)
    # photo_image_url = Column(String)

    cart = relationship("ShoppingCart", back_populates="products")
