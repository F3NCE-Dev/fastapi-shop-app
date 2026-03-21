from fastapi import APIRouter
from repositories.user import UserRepository
from schemas.user import User
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["User"])

@router.get("/users/me")
async def get_current_user(current_user: CurrentUser, db: DBSession) -> User:
    return await UserRepository.get_user(current_user.id, db)
