from fastapi import APIRouter, Depends

from repositories.AuthorizatationRepository import AuthRepository
from schemas.user import UserAuth
from schemas.responses import StatusResponse, LoginResponse
from dependencies import DBSession

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authorization"])

@router.post("/register", response_model=StatusResponse)
async def register(data: UserAuth, db: DBSession):
    user_id = await AuthRepository.register(data=data, db=db)
    return {"success": True, "detail": f"User {user_id} registered successfully"}

@router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBSession):
    credentials = UserAuth(
        username=form_data.username,
        password=form_data.password,
    )

    token = await AuthRepository.login_user(credentials, db) 
    return {"access_token": token, "token_type": "bearer"}
