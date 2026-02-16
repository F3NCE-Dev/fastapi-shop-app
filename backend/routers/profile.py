from fastapi import APIRouter, UploadFile

from repositories.profile import ProfileEdit
from schemas.responses import LoginResponse, StatusResponse
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

@router.post("/edit-profile-picture", response_model=StatusResponse)
async def edit_profile_picture(data: UploadFile, current_user: CurrentUser, db: DBSession):
    await ProfileEdit.EditProfilePicture(data, current_user.id, db)
    return {"success": True, "detail": "Profile picture updated successfully"}

@router.get("/users/{user_id}/profile-picture")
async def get_profile_picture(user_id: int, db: DBSession) -> str:
    return await ProfileEdit.GetProfilePicture(user_id, db)
