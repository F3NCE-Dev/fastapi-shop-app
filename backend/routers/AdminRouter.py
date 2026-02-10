from fastapi import APIRouter, Depends

from repositories.AdminRepository import AdminCommands
from schemas.product import ProductBase
from schemas.responses import StatusRespones

from dependencies import DBSession

router = APIRouter(tags=["Admin"])

@router.post("/add-new-product", response_model=StatusRespones)
async def admin_add_new_product(data: ProductBase, db: DBSession):
    product_id = await AdminCommands.add_new_product(data=data, db=db)
    return {"success": True, "detail": f"Product {product_id} added successfully"}
