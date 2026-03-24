from fastapi import APIRouter, Query

from app.repositories.cart import CartRepository
from app.schemas.product import ProductAdd
from app.schemas.responses import StatusResponse
from app.schemas.cart import Cart
from app.dependencies import CurrentUser, DBSession

from typing import Optional

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/items", response_model=StatusResponse, status_code=201)
async def add_to_cart(current_user: CurrentUser, item: ProductAdd, db: DBSession):
    cart_id = await CartRepository.add_to_cart(current_user.id, item.product_id, item.quantity, db)
    return {"success": True, "detail": f"Product {item.product_id} added to cart {cart_id} successfully"}

@router.delete("/items/{product_id}", response_model=StatusResponse)
async def remove_from_cart(current_user: CurrentUser,
                           product_id: int,
                           db: DBSession,
                           quantity: Optional[int] = Query(None, ge=1, description="Quantity to remove, defaults to 1")
                           ):
    cart_id = await CartRepository.remove_from_cart(current_user.id, product_id, quantity, db)
    return {"success": True, "detail": f"Cart {cart_id} updated successfully"}

@router.delete("/items", response_model=StatusResponse)
async def clear_cart(current_user: CurrentUser, db: DBSession):
    cart_id = await CartRepository.clear_cart(current_user.id, db)
    return {"success": True, "detail": f"Cart {cart_id} cleared successfully"}

@router.get("/items", response_model=Cart)
async def get_cart(current_user: CurrentUser, db: DBSession):
    return await CartRepository.get_cart_items(current_user.id, db)
