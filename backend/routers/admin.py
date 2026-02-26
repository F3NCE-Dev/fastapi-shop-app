from fastapi import APIRouter

from repositories.admin import AdminCommands
from schemas.product import ProductBase
from schemas.responses import StatusResponse
from schemas.order import Order

from dependencies import DBSession, CurrentUser

router = APIRouter(tags=["Admin"])

@router.post("/add-product", response_model=StatusResponse)
async def admin_add_product(current_user: CurrentUser, data: ProductBase, db: DBSession):
    product_id = await AdminCommands.add_product(data=data, role=current_user.role, db=db)
    return {"success": True, "detail": f"Product {product_id} added successfully"}

@router.delete("/remove-product/{product_id}", response_model=StatusResponse)
async def admin_remove_product(current_user: CurrentUser, product_id: int, db: DBSession):
    product_id = await AdminCommands.remove_product(product_id=product_id, role=current_user.role, db=db)
    return {"success": True, "detail": f"Product {product_id} removed successfully"}

@router.patch("/update-product/{product_id}", response_model=StatusResponse)
async def admin_update_product(current_user: CurrentUser, product_id: int, data: ProductBase, db: DBSession):
    product_id = await AdminCommands.update_product(product_id=product_id, data=data, role=current_user.role, db=db)
    return {"success": True, "detail": f"Product {product_id} updated successfully"}

@router.get("/get-all-orders", response_model=list[Order])
async def get_orders(current_user: CurrentUser, db: DBSession):
    orders = await AdminCommands.get_all_orders(current_user.role, db)
    return orders
