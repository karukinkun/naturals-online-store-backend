from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    price = Column(Integer)
    discount_price = Column(Integer)
    stock = Column(Integer)

    brand_id = Column(Integer, ForeignKey("brands.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    brand = relationship("Brand")
    category = relationship("Category")

    images = relationship("ProductImage", back_populates="product")
    ratings = relationship("Rating", back_populates="product")
