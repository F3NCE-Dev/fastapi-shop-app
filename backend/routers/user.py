from fastapi import APIRouter

from dependencies import DBSession
from schemas.product import ProductBase
from repositories.user import UserRepository

router = APIRouter(tags=["User Data"])

@router.get("/products", response_model=list[ProductBase])
async def get_products(db: DBSession):
    return await UserRepository.get_all_products(db)
