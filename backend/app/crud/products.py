from sqlalchemy.orm import Session
from app.models.product import Product

def get_products(db: Session, word: str, skip: int = 0, limit: int = 6):
    query = db.query(Product)

    if word:
    query = query.filter(Product.title.contains(word))

    total = query.count()

    products = query.offset(skip).limit(limit).all()

    return products, total
    