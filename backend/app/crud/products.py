from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.products import Product
from app.models.ratings import Rating


def get_products(db: Session, word: str, page: int, limit: int):
    # 商品表示数の上限制御
    limit = min(limit, 1000)
    query = (
        db.query(
            Product,
            func.avg(Rating.rating).label("avg_rating"),
        )
        .outerjoin(Rating, Product.id == Rating.product_id)
        .group_by(Product.id)
    )

    # 検索
    if word:
        for w in word.split():
            query = query.filter(Product.name.ilike(f"%{w}%"))

    total = query.count()

    products = query.offset(page - 1).limit(limit).all()

    return products, total


def get_product_detail(db: Session, product_id: int):
    result = (
        db.query(
            Product,
            func.avg(Rating.rating).label("avg_rating"),
        )
        .outerjoin(Rating, Product.id == Rating.product_id)
        .options(
            joinedload(Product.brand),
            joinedload(Product.category),
            joinedload(Product.images),
        )
        .filter(Product.id == product_id)
        .group_by(Product.id)
        .first()
    )

    return result
