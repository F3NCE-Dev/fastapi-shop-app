from pydantic import BaseModel, Field

class CartItem(BaseModel):
    product_id: int
    quantity: int
    