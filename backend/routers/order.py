from fastapi import APIRouter

from repositories.order import OrderRepository
from schemas.order import Order
from schemas.responses import StatusResponse
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Ordering"])

@router.post("/order", response_model=StatusResponse)
async def set_order(current_user: CurrentUser, db: DBSession):
    order_id = await OrderRepository.add_order(current_user.id, db)
    return {"success": True, "detail": f"Order {order_id} set successfully"}

@router.get("/order", response_model=list[Order])
async def get_order(current_user: CurrentUser, db: DBSession):
    return await OrderRepository.get_order(current_user.id, db)

@router.delete("/order/{order_id}", response_model=StatusResponse)
async def delete_order(current_user: CurrentUser, order_id: int, db: DBSession):
    await OrderRepository.delete_order(current_user.id, order_id, db)
    return {"success": True, "detail": f"Order {order_id} deleted successfully"}
