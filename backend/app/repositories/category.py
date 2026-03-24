from fastapi import HTTPException

from app.models.category import CategoryORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.category import CategoryResponse

class CategoryRepository:
    @classmethod
    async def get_all_categories(cls, db: AsyncSession) -> list[CategoryResponse]:
        result = await db.execute(select(CategoryORM))
        categories = result.scalars().all()
        
        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
            
        return categories
