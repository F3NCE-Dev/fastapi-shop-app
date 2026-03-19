from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="product name")
    description: Optional[str] = Field(description="product description")
    price: float = Field(gt=0, description="product price")
    category_id: Optional[int] = Field(gt=0, description="product category")

    model_config = ConfigDict(from_attributes=True)

class ProductAdd(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class ProductResponse(ProductBase):
    id: int
    image_url: str
