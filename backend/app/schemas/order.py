from pydantic import BaseModel, ConfigDict
from app.enums.order_status import OrderStatus
from datetime import datetime

class OrderItem(BaseModel):
    id: int
    quantity: int
    product_id: int
    order_id: int
    price_at_purchase: int

    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    total_price: float
    id: int
    user_id: int
    status: OrderStatus
    items: list[OrderItem]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
