from fastapi import APIRouter, Query
from app.schemas.products import Product, ProductsResponse

router = APIRouter(prefix="/products", tags=["products"])


mock_products = [
    {
        "id": 1,
        "title": "ナチュラルウッドボウル",
        "description": "天然素材の温かみあるボウル",
        "price": 1200,
        "rating": 4.5,
        "brand": "Natulalis",
        "category": "kitchen",
        "thumbnail": "https://example.com/img1.jpg",
    },
    {
        "id": 2,
        "title": "リネンコースター",
        "description": "吸水性の高いリネン素材",
        "price": 800,
        "rating": 4.2,
        "brand": "Natulalis",
        "category": "kitchen",
        "thumbnail": "https://example.com/img2.jpg",
    },
]


@router.get("/", response_model=ProductsResponse)
def get_products(word: str = Query("", description="検索ワード")):
    filtered = [
        p for p in mock_products
        if word.lower() in p["title"].lower()
    ]

    return {
        "products": filtered,
        "total": len(filtered),
        "skip": 0,
        "limit": 10,
    }