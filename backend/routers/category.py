from fastapi import APIRouter
from dependencies import DBSession
from schemas.category import CategoryResponse
from repositories.category import CategoryRepository

router = APIRouter(tags=["Category"])

@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(db: DBSession):
    return await CategoryRepository.get_all_categories(db)
