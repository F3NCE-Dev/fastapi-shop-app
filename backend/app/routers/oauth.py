from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi import Body

from app.auth.oauth import generate_google_oauth_uri
from app.repositories.oauth import OAuthRepository
from app.schemas.responses import AccessTokenResponse
from app.dependencies import DBSession

from typing import Annotated

router = APIRouter(tags=["OAuth2"])

@router.get("/google/url", response_class=RedirectResponse)
def get_google_oauth_url():
    return RedirectResponse(url=generate_google_oauth_uri(), status_code=302)

@router.post("/google/callback", response_model=AccessTokenResponse)
async def handle_code(code: Annotated[str, Body(embed=True)], db: DBSession):
    token = await OAuthRepository.oauth_google_login_register(code, db)
    return {"access_token": token, "token_type": "bearer"}
