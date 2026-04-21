from datetime import datetime

from pydantic import BaseModel


class RatingResponse(BaseModel):
    id: int
    product_id: int
    user_id: int | None = None
    rating: int
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RatingsResponse(BaseModel):
    ratings: list[RatingResponse]
    total: int
    page: int
    limit: int
