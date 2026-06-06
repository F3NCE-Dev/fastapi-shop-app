import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_user, auth_header


class TestGetMe:
    async def test_get_me_authenticated(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="meuser")
        resp = await client.get("/users/me", headers=auth_header(user))
        assert resp.status_code == 200
        assert resp.json()["username"] == "meuser"

    async def test_get_me_unauthenticated(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/users/me")
        assert resp.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/users/me", headers={"Authorization": "Bearer not.a.token"})
        assert resp.status_code == 401
