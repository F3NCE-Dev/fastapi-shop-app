from pydantic import BaseModel, ConfigDict

class OrderItem(BaseModel):
    id: int
    quantity: int
    product_id: int
    order_id: int
    price_at_purchase: int

    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    total_price: int
    id: int
    user_id: int
    items: list[OrderItem]

    model_config = ConfigDict(from_attributes=True)
