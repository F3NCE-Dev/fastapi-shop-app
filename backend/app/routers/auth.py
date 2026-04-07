from fastapi import APIRouter, Depends, Response, HTTPException, Cookie

from app.repositories.auth import AuthRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserAuth
from app.schemas.responses import StatusResponse, AccessTokenResponse
from app.dependencies import DBSession
from app.config.config import settings

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authorization"])

@router.post("/register", response_model=StatusResponse, status_code=201)
async def register(data: UserAuth, db: DBSession):
    user_id = await AuthRepository.register(data=data, db=db)
    return {"success": True, "detail": f"User {user_id} registered successfully"}

@router.post("/login", response_model=AccessTokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBSession, response: Response):
    credentials = UserAuth(
        username=form_data.username,
        password=form_data.password,
    )

    access_token, refresh_token = await AuthRepository.login_user(credentials, db) 
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age = settings.REFRESH_TOKEN_MAX_AGE
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh(
    db: DBSession, 
    response: Response, 
    refresh_token: Annotated[str | None, Cookie()] = None
):
    try:
        access_token, new_refresh_token = await UserRepository.refresh_token(refresh_token, db)
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age = settings.REFRESH_TOKEN_MAX_AGE
    )

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    db: DBSession, 
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None
):
    await UserRepository.logout(refresh_token, db)

    response.delete_cookie("refresh_token")

    return {"success": True, "detail": "Logged out successfully"}
