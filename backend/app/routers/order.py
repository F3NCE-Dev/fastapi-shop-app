from fastapi import APIRouter

from app.repositories.order import OrderRepository
from app.schemas.order import Order
from app.schemas.responses import StatusResponse
from app.dependencies import CurrentUser, DBSession

router = APIRouter(prefix="/orders", tags=["Ordering"])

@router.post("", response_model=StatusResponse, status_code=201)
async def set_order(current_user: CurrentUser, db: DBSession):
    order_id = await OrderRepository.add_order(current_user.id, db)
    return {"success": True, "detail": f"Order {order_id} set successfully"}

@router.get("", response_model=list[Order])
async def get_orders(current_user: CurrentUser, db: DBSession):
    return await OrderRepository.get_orders(current_user.id, db)

@router.delete("/{order_id}", response_model=StatusResponse)
async def delete_order(current_user: CurrentUser, order_id: int, db: DBSession):
    await OrderRepository.delete_order(current_user.id, order_id, db)
    return {"success": True, "detail": f"Order {order_id} deleted successfully"}
