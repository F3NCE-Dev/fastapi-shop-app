import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_user, auth_header


class TestProfile:
    async def test_edit_profile_username(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="profileuser1", password="pass123")
        resp = await client.patch(
            "/profile",
            data={"new_username": "profileuser1_renamed"},
            headers=auth_header(user),
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_edit_profile_password(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="profileuser3", password="oldpass")
        resp = await client.patch(
            "/profile",
            data={"new_password": "newpass99"},
            headers=auth_header(user),
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_edit_profile_unauthenticated(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.patch("/profile", data={"new_username": "hacker"})
        assert resp.status_code == 401

    async def test_edit_profile_invalid_username_raises_validation_error(self, client: AsyncClient, db_session: AsyncSession):
        from pydantic import ValidationError
        user = await create_user(db_session, username="profileuser2")
        # The router instantiates UserUpdate(username=new_username) directly in the handler
        # body — outside FastAPI's request-parsing layer — so an invalid username bypasses
        # the 422 machinery and raises a raw Pydantic ValidationError that propagates out.
        with pytest.raises(ValidationError):
            await client.patch(
                "/profile",
                data={"new_username": "bad name!"},
                headers=auth_header(user),
            )
