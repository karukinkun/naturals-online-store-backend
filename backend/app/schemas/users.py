from datetime import date, datetime
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


class UserRankResponse(BaseModel):
    code: str
    name: str
    image_url: str | None = None
    point_rate: int


class UserPaymentMethodResponse(BaseModel):
    code: str
    name: str


class UserCreateResponse(BaseModel):
    id: UUID
    cognito_sub: str
    email: str
    default_payment_method: str


class UserResponse(BaseModel):
    id: UUID
    cognito_sub: str

    last_name: str
    first_name: str
    gender: str
    birthday: date

    postal_code: str
    prefecture: str
    address1: str
    address2: str
    address3: str | None = None

    email: str
    phone_number: str | None = None

    points: int
    rank: UserRankResponse | None = None
    default_payment_method: UserPaymentMethodResponse | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
