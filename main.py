from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/items/")
def create_item(item_name: str, item_price: float, item_description: str = '', item_quantity: int = 0,
                db: Session = Depends(get_db)):
    return crud.create_item(db, item_name, item_price, item_description, item_quantity)


@app.get("/items/")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/brands/")
def create_brand(brand_name: str, db: Session = Depends(get_db)):
    return crud.create_brand(db, brand_name)


@app.get("/brands/")
def read_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip=skip, limit=limit)
    return brands


@app.post("/categories/")
def create_category(category_name: str, db: Session = Depends(get_db)):
    return crud.create_category(db, category_name)


@app.get("/categories/")
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.post("/supplies/")
def create_supply(item_id: int, supply_quantity: int, supply_date: datetime = datetime.now(), db: Session = Depends(get_db)):
    return crud.create_supply(db, item_id, supply_quantity, supply_date)


@app.get("/supplies/")
def read_supplies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    supplies = crud.get_supplies(db, skip=skip, limit=limit)
    return supplies
