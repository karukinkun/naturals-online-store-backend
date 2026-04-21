from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer)
    comment = Column(Text)
    is_delete = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    product = relationship("Product", back_populates="ratings")
