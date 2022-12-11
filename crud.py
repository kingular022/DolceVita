from sqlalchemy.orm import Session

import models


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item_name:str, item_price:float, item_description:str ='', item_quantity:int =0):
    db_item = models.Item(name=item_name, price=item_price, description=item_description, quantity=item_quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Brand).offset(skip).limit(limit).all()


def create_brand(db: Session, brand_name:str):
    db_brand = models.Brand(name=brand_name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category_name:str):
    db_category = models.Category(name=category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
