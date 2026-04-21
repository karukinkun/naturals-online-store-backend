from sqlalchemy.orm import Session

from app.models.ratings import Rating


def get_ratings_by_product_id(db: Session, product_id: int, page: int, limit: int):
    # 商品表示数の上限制御
    limit = min(limit, 1000)
    offset = (page - 1) * limit

    query = (
        db.query(Rating)
        .filter(Rating.product_id == product_id)
        .filter(Rating.is_delete == False)
        .order_by(Rating.created_at.desc())
    )

    ratings = query.offset(offset).limit(limit).all()
    total = query.count()

    return ratings, total
