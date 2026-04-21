from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class UserRank(Base):
    __tablename__ = "user_ranks"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)

    image_url = Column(Text)
    point_rate = Column(Numeric(5, 2), nullable=False, default=1.00)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    users = relationship("User", back_populates="rank")
