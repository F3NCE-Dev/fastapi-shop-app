from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="product name")
    price: float = Field(gt=0, description="product price")
    image_url: str

    model_config = ConfigDict(from_attributes=True)

class ProductAdd(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
