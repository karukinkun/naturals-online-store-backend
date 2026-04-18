from pydantic import BaseModel

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: int
    rating: float
    brand: str
    category: str
    thumbnail: str

    class Config:
        from_attributes = True


class ProductsResponse(BaseModel):
    products: list[Product]
    total: int
    skip: int
    limit: int