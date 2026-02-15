from fastapi import APIRouter

from repositories.cart import CartRepository
from schemas.cart import AddtoCart
from schemas.responses import StatusResponse
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Cart Panel"])

@router.post("/add-to-cart", response_model=StatusResponse)
async def add_to_cart(current_user: CurrentUser, item: AddtoCart, db: DBSession):
    cart_id = await CartRepository.add_to_cart(current_user.id, item.product_id, item.quantity, db)
    return {"success": True, "detail": f"Product {item.product_id} added to cart {cart_id} successfully"}
