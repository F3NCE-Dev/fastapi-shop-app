from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM

from app.auth.security import create_access_token, hash_password
from app.config.config import settings

import httpx
import jwt
import re
import secrets

class OAuthRepository:
    @classmethod
    async def oauth_google_login_register(cls, code: str, db: AsyncSession) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://oauth2.googleapis.com/token",
                data={
                    "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
                    "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.REDIRECT_URI,
                    "code": code,
                })
            res = response.json()
        
            if "error" in res:
                raise HTTPException(status_code=400, detail=res.get("error_description", "OAuth error"))

            id_token = res["id_token"]
            user_data = jwt.decode(id_token, algorithms=["RS256"], options={"verify_signature": not settings.DEBUG_MODE})
            
            email = user_data.get("email")
            name = user_data.get("name") or user_data.get("given_name")

            if not email:
                raise HTTPException(status_code=400, detail="Email not found in token")

            result = await db.execute(select(UserORM).where(UserORM.email == email))
            user = result.scalar_one_or_none()

            if user:
                return create_access_token({"sub": user.username})

            base_name = name if name else email.split("@")[0]
            clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', base_name)
            if not clean_name:
                clean_name = "user"

            username = clean_name
            counter = 1

            while True:
                res = await db.execute(select(UserORM).where(UserORM.username == username))
                if not res.scalar_one_or_none():
                    break
                username = f"{clean_name}{counter}"
                counter += 1

            random_password = secrets.token_urlsafe(16)
            user = UserORM(username=username, password=hash_password(random_password), email=email)
            db.add(user)
            await db.commit()

            return create_access_token({"sub": user.username})
    