from fastapi import HTTPException
from app.dependencies import get_image_url
from app.schemas.product import ProductResponse
from app.models.product import ProductORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class ProductRepository:
    @classmethod
    async def get_products(cls, category_id: int, search: str, limit: int, offset: int, sort: Optional[str], db: AsyncSession) -> list[ProductResponse]:
        query = select(ProductORM)
        
        if category_id:
            query = query.where(ProductORM.category_id == category_id)
        if search:
            query = query.where(ProductORM.name.ilike(f"%{search}%"))

        if sort:
            descending = sort.startswith("-")
            field = sort.lstrip("-")
            
            if hasattr(ProductORM, field):
                column = getattr(ProductORM, field)
                query = query.order_by(column.desc() if descending else column.asc())

        query = query.limit(limit).offset(offset)

        result = await db.execute(query)
        products = result.scalars().all()

        for product in products:
            product.image_url = get_image_url(product.image_url)
        
        return products

    @classmethod
    async def get_product(cls, product_id: int, db: AsyncSession) -> ProductResponse:
        result = await db.execute(select(ProductORM).where(ProductORM.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product.image_url = get_image_url(product.image_url)

        return product
