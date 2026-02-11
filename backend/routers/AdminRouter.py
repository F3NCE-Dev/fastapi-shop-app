from fastapi import APIRouter

from repositories.AdminRepository import AdminCommands
from schemas.product import ProductBase
from schemas.responses import StatusRespones

from dependencies import DBSession

router = APIRouter(tags=["Admin"])

@router.post("/add-product", response_model=StatusRespones)
async def admin_add_product(data: ProductBase, db: DBSession):
    product_id = await AdminCommands.add_product(data=data, db=db)
    return {"success": True, "detail": f"Product {product_id} added successfully"}

@router.delete("/remove-product/{product_id}", response_model=StatusRespones)
async def admin_remove_product(product_id: int, db: DBSession):
    product_id = await AdminCommands.remove_product(product_id=product_id, db=db)
    return {"success": True, "detail": f"Product {product_id} removed successfully"}
