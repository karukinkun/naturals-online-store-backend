from pydantic import BaseModel


class Image(BaseModel):
    id: int
    image_url: str


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: int
    discount_price: int | None = None
    stock: int | None = None
    brand_id: int
    brand: str | None = None
    category_id: int
    category: str | None = None
    rating: float | None = None
    images: list[Image]

    class Config:
        from_attributes = True


class ProductsResponse(BaseModel):
    products: list[Product]
    total: int
    page: int
    limit: int
