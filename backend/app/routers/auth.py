from fastapi import APIRouter, Depends

from app.repositories.auth import AuthRepository
from app.schemas.user import UserAuth
from app.schemas.responses import StatusResponse, LoginResponse
from app.dependencies import DBSession

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authorization"])

@router.post("/register", response_model=StatusResponse, status_code=201)
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
