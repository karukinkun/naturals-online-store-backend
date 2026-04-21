from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    image_url: str | None = None

    class Config:
        from_attributes = True


class CategoriesResponse(BaseModel):
    categories: list[CategoryResponse]
