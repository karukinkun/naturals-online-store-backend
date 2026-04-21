from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.categories import get_categories
from app.db.database import SessionLocal
from app.schemas.categories import CategoriesResponse
from app.utils.storage import build_image_url

router = APIRouter(prefix="/categories", tags=["categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=CategoriesResponse)
def read_categories(db: Session = Depends(get_db)):
    categories = get_categories(db)

    return {
        "categories": [
            {
                "id": category.id,
                "name": category.name,
                "image_url": build_image_url(category.image_url),
            }
            for category in categories
        ]
    }
