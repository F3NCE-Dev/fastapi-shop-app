from fastapi import HTTPException
from redis.asyncio import Redis

from app.models.category import CategoryORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.category import CategoryResponse

import json

class CategoryRepository:
    @classmethod
    async def get_all_categories(cls, db: AsyncSession, redis: Redis) -> list[CategoryResponse]:
        cached = await redis.get("categories")
        if cached:
            return [CategoryResponse(**c) for c in json.loads(cached)]

        result = await db.execute(select(CategoryORM))
        categories = result.scalars().all()
        
        if not categories:
            raise HTTPException(status_code=404, detail="Categories not found")
        
        await redis.set("categories", json.dumps([CategoryResponse.model_validate(c).model_dump() for c in categories]), ex=600)
        return categories
