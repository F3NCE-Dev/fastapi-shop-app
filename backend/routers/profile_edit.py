from fastapi import APIRouter

from repositories.profile import ProfileEdit
from schemas.responses import LoginResponse
from schemas.user import NewUsername, NewPassword
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Profile edit"])

@router.patch("/edit-username", response_model=LoginResponse)
async def edit_username(new_username: NewUsername, current_user: CurrentUser, db: DBSession):
    token = await ProfileEdit.EditUsername(new_username.new_name, current_user.id, db)
    return {"access_token": token, "token_type": "bearer"}

@router.patch("/edit-password", response_model=LoginResponse)
async def edit_password(current_user: CurrentUser, new_password: NewPassword, db: DBSession):
    token = await ProfileEdit.EditPassword(current_user.id, new_password.password, db)
    return {"access_token": token, "token_type": "bearer"}
