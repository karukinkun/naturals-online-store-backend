from sqlalchemy.orm import Session

from app.models.categories import Category


def get_categories(db: Session):
    return db.query(Category).order_by(Category.id.asc()).all()
