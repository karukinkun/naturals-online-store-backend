import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cognito_sub = Column(String(255), nullable=False, unique=True)

    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    birthday = Column(Date, nullable=False)

    postal_code = Column(String(7), nullable=False)
    prefecture = Column(String(20), nullable=False)
    address1 = Column(String(255), nullable=False)
    address2 = Column(String(255), nullable=False)
    address3 = Column(String(255))

    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(20))

    points = Column(Integer, nullable=False, default=0)

    rank_id = Column(Integer, ForeignKey("user_ranks.id"))

    is_active = Column(Boolean, nullable=False, default=True)
    deleted_at = Column(DateTime)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    payment_methods = relationship("UserPaymentMethod", back_populates="user")
    rank = relationship("UserRank", back_populates="users")

    __table_args__ = (
        CheckConstraint("postal_code ~ '^[0-9]{7}$'", name="check_postal_code_format"),
        CheckConstraint("points >= 0", name="check_points_positive"),
    )
