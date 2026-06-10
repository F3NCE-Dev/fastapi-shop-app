from fastapi import APIRouter
from app.repositories.user import UserRepository
from app.schemas.user import User
from app.dependencies import CurrentUser, DBSession, REDIS

router = APIRouter(tags=["User"])

@router.get("/users/me")
async def get_current_user(current_user: CurrentUser, db: DBSession, redis: REDIS) -> User:
    return await UserRepository.get_user(current_user.id, db, redis)
