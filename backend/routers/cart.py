from fastapi import APIRouter

from repositories.cart import CartRepository
from schemas.product import ProductAdd
from schemas.responses import StatusResponse
from schemas.cart import Cart
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Cart Panel"])

@router.post("/cart/items", response_model=StatusResponse, status_code=201)
async def add_to_cart(current_user: CurrentUser, item: ProductAdd, db: DBSession):
    cart_id = await CartRepository.add_to_cart(current_user.id, item.product_id, item.quantity, db)
    return {"success": True, "detail": f"Product {item.product_id} added to cart {cart_id} successfully"}

@router.delete("/cart/items/{product_id}", response_model=StatusResponse)
async def remove_from_cart(current_user: CurrentUser, product_id: int, db: DBSession):
    cart_id = await CartRepository.remove_from_cart(current_user.id, product_id, db)
    return {"success": True, "detail": f"Cart {cart_id} updated successfully"}

@router.delete("/cart", response_model=StatusResponse)
async def clear_cart(current_user: CurrentUser, db: DBSession):
    cart_id = await CartRepository.clear_cart(current_user.id, db)
    return {"success": True, "detail": f"Cart {cart_id} cleared successfully"}

@router.get("/cart", response_model=Cart)
async def get_cart(current_user: CurrentUser, db: DBSession):
    return await CartRepository.get_cart_items(current_user.id, db)
