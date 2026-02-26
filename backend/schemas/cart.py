from pydantic import BaseModel

class Cart(BaseModel):
    items: list[dict]
    total_price: int
