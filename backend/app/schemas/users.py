from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    # cognito_sub: str

    last_name: str
    first_name: str
    gender: str
    birthday: date

    postal_code: str = Field(pattern=r"^[0-9]{7}$")
    prefecture: str
    address1: str
    address2: str
    address3: str | None = None

    email: EmailStr
    phone_number: str | None = None


class UserCreateResponse(BaseModel):
    id: UUID
    cognito_sub: str
    email: str
    default_payment_method: str
