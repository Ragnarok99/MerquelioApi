import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from scrapper.main import search

import models
import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home():
    return {"hello": "world"}


@app.get('/shopping-carts', response_model=list[schemas.ShoppingCart], status_code=200)
def get_shopping_carts(db: Session = Depends(get_db)):
    items = db.query(models.ShoppingCart).all()
    return items


@app.post('/shopping-carts', response_model=schemas.ShoppingCart, status_code=201)
def create_shopping_cart(cart: schemas.ShoppingCartCreate, db: Session = Depends(get_db)):
    newShoppingCart = models.ShoppingCart(
        name=cart.name, created_at=datetime.datetime.now())
    db.add(newShoppingCart)
    db.commit()
    db.refresh(newShoppingCart)
    return newShoppingCart


@app.post('/shopping-carts/{cart_id}/products', response_model=schemas.ShoppingCart, status_code=200)
def add_products_to_shopping_cart(cart_id: int, products: list[schemas.ProductCreate], db: Session = Depends(get_db)):
    cart_to_add_products = db.query(models.ShoppingCart).filter(
        models.ShoppingCart.id == cart_id).first()
    if(cart_to_add_products is None):
        raise HTTPException(status_code=404, detail="shopping cart not found")
    for product in products:
        newProduct = models.Product(
            **product.dict(), cart_id=cart_id)
        db.add(newProduct)
        db.commit()
        db.refresh(newProduct)

    db.refresh(cart_to_add_products)

    return cart_to_add_products


@app.get('/shopping-carts/{cart_id}/search', status_code=200)
def search_cart_products(cart_id: int, db: Session = Depends(get_db)):
    shopping_cart = db.query(models.ShoppingCart).filter(
        models.ShoppingCart.id == cart_id).first()

    if(shopping_cart is None):
        raise HTTPException(status_code=404, detail="shopping cart not found")

    result = search(shopping_cart.products)
    print(result)
    return result
