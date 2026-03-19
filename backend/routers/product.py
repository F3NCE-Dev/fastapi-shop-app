from fastapi import APIRouter, Query
from typing import Optional

from dependencies import DBSession
from schemas.product import ProductResponse
from repositories.product import ProductRepository

router = APIRouter(tags=["Product Data"])

@router.get("/products", response_model=list[ProductResponse])
async def get_products(
                       db: DBSession,
                       category: Optional[str] = Query(None, description="Filter by category"),
                       search: Optional[str] = Query(None, description="Search by name"),
                       limit: int = Query(10, ge=1, le=100),
                       offset: int = Query(0, ge=0),
                       sort: Optional[str] = Query(None, description="Sort field, use - for descending")
                       ):
    return await ProductRepository.get_products(category, search, limit, offset, sort, db)

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: DBSession):
    return await ProductRepository.get_product(product_id, db)
