from fastapi import APIRouter, Query
from typing import Optional

from app.dependencies import DBSession
from app.schemas.product import ProductResponse
from app.repositories.product import ProductRepository

router = APIRouter(prefix="/products", tags=["Product Data"])

@router.get("", response_model=list[ProductResponse])
async def get_products(
                       db: DBSession,
                       category_id: Optional[int] = Query(None, description="Filter by category"),
                       search: Optional[str] = Query(None, description="Search by name"),
                       limit: int = Query(10, ge=1, le=100),
                       offset: int = Query(0, ge=0),
                       sort: Optional[str] = Query(None, description="Sort field, use - for descending")
                       ):
    return await ProductRepository.get_products(category_id, search, limit, offset, sort, db)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: DBSession):
    return await ProductRepository.get_product(product_id, db)
