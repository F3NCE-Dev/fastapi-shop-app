from fastapi import APIRouter
from app.dependencies import DBSession, REDIS
from app.schemas.category import CategoryResponse
from app.repositories.category import CategoryRepository

router = APIRouter(tags=["Category"])

@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(db: DBSession, redis: REDIS):
    return await CategoryRepository.get_all_categories(db, redis)
