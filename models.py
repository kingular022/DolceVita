from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(DECIMAL(scale=2))
    quantity = Column(Integer)

    category_id = Column(Integer, ForeignKey('Categories.id'))
    category = relationship('Category', back_populates='items')
    brand_id = Column(Integer, ForeignKey('Brands.id'))
    brand = relationship('Brand', back_populates='items')

class Category(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    items = relationship('Item', back_populates='category')

class Brand(Base):
    __tablename__ = "Brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    items = relationship('Item', back_populates='brand')