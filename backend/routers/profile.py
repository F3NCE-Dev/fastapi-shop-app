from fastapi import APIRouter, UploadFile, Form

from repositories.profile import ProfileEdit
from schemas.responses import LoginResponse, StatusResponse
from schemas.user import UserUpdate
from dependencies import CurrentUser, DBSession

router = APIRouter(tags=["Profile"])

@router.patch("/profile", response_model=LoginResponse)
async def edit_profile(current_user: CurrentUser,
                       db: DBSession,
                       new_username: str | None = Form(None),
                       new_password: str | None = Form(None)
                       ):
    data = UserUpdate(username=new_username, password=new_password)
    token = await ProfileEdit.EditProfile(profile_id=current_user.id, data=data, db=db)
    return LoginResponse(access_token=token, token_type="bearer")

@router.patch("/profile/image", response_model=StatusResponse)
async def update_profile_image(current_user: CurrentUser, image: UploadFile, db: DBSession):
    await ProfileEdit.UpdateProfileImage(profile_id=current_user.id, image=image, db=db)
    return {"success": True, "detail": "Profile image updated successfully"}
