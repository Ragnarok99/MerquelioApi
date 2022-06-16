import datetime
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    quantity: int
    # price: str
    # photo_image_url: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    cart_id: int

    class Config:
        orm_mode = True


class ShoppingCartBase(BaseModel):
    name: str


class ShoppingCartCreate(ShoppingCartBase):
    pass


class ShoppingCart(ShoppingCartBase):
    id: int
    products: list[Product] = []
    created_at: datetime.date

    class Config:
        orm_mode = True
