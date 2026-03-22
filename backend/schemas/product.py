from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

nameStr = Annotated[str, Field(min_length=1, max_length=100, description="product name")]
descriptionStr = Annotated[str, Field(max_length=1000, description="product description")]
priceFloat = Annotated[float, Field(gt=0, description="product price")]
categoryId = Annotated[int, Field(gt=0, description="product category")]

class ProductBase(BaseModel):
    name: nameStr
    description: descriptionStr | None = None
    price: priceFloat
    category_id: categoryId | None = None

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    name: nameStr | None = None
    description: descriptionStr | None = None
    price: priceFloat | None = None
    category_id: categoryId | None = None

class ProductAdd(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class ProductResponse(ProductBase):
    id: int
    image_url: str
