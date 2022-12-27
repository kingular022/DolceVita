from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import models


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def delete_item(db: Session, item_id: int):
    try:
        deleted = db.query(models.Item).filter(models.Item.id == item_id).delete()
        db.commit()
        if deleted:
            return f"Deleted item with id: {item_id}"
        else:
            return f"No item with id: {item_id}"
    except SQLAlchemyError:
        return 'Ups, coś poszło nie tak'


def update_item(db: Session, item_id: int, item_name: str | None = None,
                item_price: float | None = None, item_description: str | None = None,
                item_quantity: int | None = None,
                category_id: int | None = None, brand_id: int | None = None):
    db_item = db.query(models.Item).get(item_id)
    if db_item is not None:
        if item_name is not None:
            db_item.name = item_name
        if item_price is not None:
            db_item.price = item_price
        if item_description is not None:
            db_item.description = item_description
        if item_quantity is not None:
            db_item.quantity = item_quantity
        if category_id is not None:
            db_category = db.query(models.Category).get(category_id)
            if db_category is not None:
                db_item.category = db_category
            else:
                raise HTTPException(status_code=404, detail="Category not found")
        if brand_id is not None:
            db_brand = db.query(models.Brand).get(brand_id)
            if db_brand is not None:
                db_item.brand = db_brand
            else:
                raise HTTPException(status_code=404, detail="Brand not found")
        try:
            db.commit()
            db.refresh(db_item)
            return db_item
        except SQLAlchemyError:
            return 'Ups, coś poszło nie tak'
    else:
        raise HTTPException(status_code=404, detail="Item not found")


def create_item(db: Session, item_name: str, item_price: float, item_description: str = '', item_quantity: int = 0,
                category_id: int | None = None, brand_id: int | None = None):
    db_new_item = models.Item(name=item_name, price=item_price, description=item_description, quantity=item_quantity)
    if category_id is not None:
        db_category = db.query(models.Category).get(category_id)
        if db_category is not None:
            db_new_item.category = db_category
        else:
            raise HTTPException(status_code=404, detail="Category not found")
    if brand_id is not None:
        db_brand = db.query(models.Brand).get(brand_id)
        if db_brand is not None:
            db_new_item.brand = db_brand
        else:
            raise HTTPException(status_code=404, detail="Brand not found")

    try:
        db.add(db_new_item)
        db.commit()
        db.refresh(db_new_item)
        return db_new_item
    except SQLAlchemyError:
        return 'Ups, coś poszło nie tak'


def get_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Brand).offset(skip).limit(limit).all()


def create_brand(db: Session, brand_name: str):
    db_brand = models.Brand(name=brand_name)
    try:
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand
    except SQLAlchemyError:
        return 'Ups, coś poszło nie tak'


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category_name: str):
    db_category = models.Category(name=category_name)
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except SQLAlchemyError:
        return 'Ups, coś poszło nie tak'


def get_supplies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_supply(db: Session, item_id: int, supply_quantity: int, supply_date: datetime = datetime.now()):
    db_item = db.query(models.Item).get(item_id)
    if db_item is not None:
        db_supply = models.Supply(quantity=supply_quantity, date=supply_date, item=db_item)
        try:
            db.add(db_supply)
            db_item.quantity += supply_quantity
            db.commit()
            db.refresh(db_supply)
            return db_supply
        except SQLAlchemyError:
            return 'Ups, coś poszło nie tak'
    else:
        raise HTTPException(status_code=404, detail="Item not found")
