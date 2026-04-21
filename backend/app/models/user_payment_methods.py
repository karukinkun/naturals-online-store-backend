import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class UserPaymentMethod(Base):
    __tablename__ = "user_payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    payment_method_id = Column(
        Integer, ForeignKey("payment_methods.id"), nullable=False
    )

    provider = Column(String(50), nullable=False, default="manual")

    provider_customer_id = Column(String(255))
    provider_payment_method_id = Column(String(255))

    card_brand = Column(String(50))
    card_last4 = Column(String(4))
    card_exp_month = Column(Integer)
    card_exp_year = Column(Integer)

    is_default = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    deleted_at = Column(DateTime)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="payment_methods")
    payment_method = relationship(
        "PaymentMethod", back_populates="user_payment_methods"
    )
