from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud.ratings import get_ratings_by_product_id
from app.db.database import SessionLocal
from app.schemas.ratings import RatingsResponse

router = APIRouter(prefix="/products", tags=["ratings"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{product_id}/ratings", response_model=RatingsResponse)
def read_ratings_by_product_id(
    product_id: int,
    page: Annotated[int, Query(ge=1, description="開始位置")] = 1,
    limit: Annotated[int, Query(ge=1, le=1000, description="取得件数")] = 5,
    db: Session = Depends(get_db),
):
    ratings, total = get_ratings_by_product_id(db, product_id, page, limit)

    return {
        "ratings": ratings,
        "total": total,
        "page": page,
        "limit": limit,
    }
