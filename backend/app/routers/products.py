from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.products import get_product_detail, get_products
from app.db.database import SessionLocal
from app.schemas.products import Product, ProductsResponse
from app.utils.storage import build_image_url

router = APIRouter(prefix="/products", tags=["products"])


# DBセッション
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=ProductsResponse)
def read_products(
    word: Annotated[str, Query(max_length=100, description="検索ワード")] = "",
    page: Annotated[int, Query(ge=1, description="開始位置")] = 1,
    limit: Annotated[int, Query(ge=1, le=1000, description="取得件数")] = 50,
    db: Session = Depends(get_db),
):
    products, total = get_products(db, word, page, limit)

    result = []
    for product, avg_rating in products:
        result.append(
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "discount_price": product.discount_price,
                "stock": product.stock,
                "brand_id": product.brand.id,
                "brand": product.brand.name if product.brand else None,
                "category_id": product.category.id,
                "category": product.category.name if product.category else None,
                "rating": round(avg_rating, 1) if avg_rating else None,
                "images": [
                    {
                        "id": img.id,
                        "image_url": build_image_url(img.image_url),
                    }
                    for img in product.images
                ],
            }
        )

    return {
        "products": result,
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{product_id}", response_model=Product)
def read_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
):
    result = get_product_detail(db, product_id)

    if not result:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    product, avg_rating = result

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "discount_price": product.discount_price,
        "stock": product.stock,
        "brand_id": product.brand.id if product.brand else None,
        "brand": product.brand.name if product.brand else None,
        "category_id": product.category.id if product.category else None,
        "category": product.category.name if product.category else None,
        "rating": round(avg_rating, 1) if avg_rating else None,
        "images": [
            {
                "id": img.id,
                "image_url": build_image_url(img.image_url),
            }
            for img in product.images
        ],
    }
