from fastapi import APIRouter, Depends

from repositories.admin import AdminCommands
from schemas.product import ProductBase
from schemas.responses import StatusResponse
from schemas.order import Order
from enums.order_status import OrderStatus
from permissions.permissions import admin_required
from dependencies import DBSession

router = APIRouter(tags=["Admin"], dependencies=[Depends(admin_required)])

@router.post("/add-product", response_model=StatusResponse)
async def admin_add_product(data: ProductBase, db: DBSession):
    product_id = await AdminCommands.add_product(data=data, db=db)
    return {"success": True, "detail": f"Product {product_id} added successfully"}

@router.delete("/remove-product/{product_id}", response_model=StatusResponse)
async def admin_remove_product(product_id: int, db: DBSession):
    product_id = await AdminCommands.remove_product(product_id=product_id, db=db)
    return {"success": True, "detail": f"Product {product_id} removed successfully"}

@router.patch("/update-product/{product_id}", response_model=StatusResponse)
async def admin_update_product(product_id: int, data: ProductBase, db: DBSession):
    product_id = await AdminCommands.update_product(product_id=product_id, data=data, db=db)
    return {"success": True, "detail": f"Product {product_id} updated successfully"}

@router.patch("/orders/{order_id}/status", response_model=StatusResponse)
async def admin_update_order_status(order_id: int, status: OrderStatus, db: DBSession):
    order_id = await AdminCommands.update_order_status(order_id=order_id, status=status, db=db)
    return {"success": True, "detail": f"Order {order_id} updated successfully"}

@router.get("/orders", response_model=list[Order])
async def get_orders(db: DBSession):
    orders = await AdminCommands.get_all_orders(db)
    return orders
