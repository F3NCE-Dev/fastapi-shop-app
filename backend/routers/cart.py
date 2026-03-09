from fastapi import APIRouter

from repositories.cart import CartRepository
from schemas.product import ProductAdd
from schemas.responses import StatusResponse
from schemas.cart import Cart
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Cart Panel"])

@router.post("/add-to-cart", response_model=StatusResponse)
async def add_to_cart(current_user: CurrentUser, item: ProductAdd, db: DBSession):
    cart_id = await CartRepository.add_to_cart(current_user.id, item.product_id, item.quantity, db)
    return {"success": True, "detail": f"Product {item.product_id} added to cart {cart_id} successfully"}

@router.delete("/clear-cart", response_model=StatusResponse)
async def clear_cart(current_user: CurrentUser, db: DBSession):
    cart_id = await CartRepository.clear_cart(current_user.id, db)
    return {"success": True, "detail": f"Cart {cart_id} cleared successfully"}

@router.get("/get-cart-items", response_model=Cart)
async def get_cart(current_user: CurrentUser, db: DBSession):
    return await CartRepository.get_cart_items(current_user.id, db)
