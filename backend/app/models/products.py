from sqlalchemy import Column, Float, Integer, String

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(500))
    price = Column(Integer)
    rating = Column(Float)
    brand = Column(String(255))
    category = Column(String(255))
    thumbnail = Column(String(500))
