from fastapi import APIRouter, Query
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import Depends

from dependencies import DBSession
from schemas.product import ProductBase
from repositories.user import UserRepository

router = APIRouter(tags=["User Data"])

@router.get("/products", response_model=list[ProductBase])
async def get_products(category: Optional[str] = Query(None, description="Filter by category"),
                       search: Optional[str] = Query(None, description="Search by name"),
                       db: AsyncSession = Depends(get_db)):
    return await UserRepository.get_products(category, search, db)

@router.get("/products/{product_id}", response_model=ProductBase)
async def get_product(product_id: int, db: DBSession):
    return await UserRepository.get_product(product_id, db)
