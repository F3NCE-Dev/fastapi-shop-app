from fastapi import APIRouter

from repositories.profile_repository import ProfileEdit
from schemas.responses import LoginResponse
from schemas.user import NewUsername
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Profile edit"])

@router.patch("/edit-username", response_model=LoginResponse)
async def edit_username(new_username: NewUsername, current_user: CurrentUser, db: DBSession):
    token = await ProfileEdit.EditUsername(new_username.new_name, current_user.id, db)
    return {"access_token": token, "token_type": "bearer"}
