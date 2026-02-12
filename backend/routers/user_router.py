from fastapi import APIRouter

from dependencies import CurrentUser
from schemas.user import UserID
from repositories.UserDataRepository import UserRepository

router = APIRouter(tags=["User Data"])

@router.get("/user", response_model=UserID)
async def get_current_user_handler(current_user: CurrentUser):
    return await UserRepository.get_user(current_user)
