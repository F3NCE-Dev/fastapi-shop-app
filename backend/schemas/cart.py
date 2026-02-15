from pydantic import BaseModel, Field

class AddtoCart(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
