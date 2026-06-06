import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_user


class TestRegister:
    async def test_register_success(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.post("/register", json={"username": "alice", "password": "pass123"})
        assert resp.status_code == 201
        body = resp.json()
        assert body["success"] is True
        # detail contains the user id, not the username — e.g. "User 3 registered successfully"
        assert "registered successfully" in body["detail"]

    async def test_register_duplicate_username(self, client: AsyncClient, db_session: AsyncSession):
        await client.post("/register", json={"username": "bob", "password": "pass123"})
        resp = await client.post("/register", json={"username": "bob", "password": "pass123"})
        # app returns 400 for duplicates, not 409
        assert resp.status_code == 400

    async def test_register_short_password(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.post("/register", json={"username": "charlie", "password": "abc"})
        assert resp.status_code == 422

    async def test_register_invalid_username_chars(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.post("/register", json={"username": "user name!", "password": "valid1"})
        assert resp.status_code == 422


class TestLogin:
    async def test_login_success(self, client: AsyncClient, db_session: AsyncSession):
        await create_user(db_session, username="loginuser", password="mypassword")
        resp = await client.post("/login", data={"username": "loginuser", "password": "mypassword"})
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient, db_session: AsyncSession):
        await create_user(db_session, username="loginuser2", password="correct")
        resp = await client.post("/login", data={"username": "loginuser2", "password": "wrong"})
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient, db_session: AsyncSession):
        # username must satisfy UserAuth constraints (min 1, max 25, alphanumeric/_/-)
        resp = await client.post("/login", data={"username": "ghost_user", "password": "nope12"})
        assert resp.status_code == 401


class TestLogout:
    async def test_logout_success(self, client: AsyncClient, db_session: AsyncSession):
        await create_user(db_session, username="logoutuser", password="pass123")
        login_resp = await client.post("/login", data={"username": "logoutuser", "password": "pass123"})
        assert login_resp.status_code == 200
        resp = await client.post("/logout")
        assert resp.status_code == 200
        assert resp.json()["success"] is True


class TestRefresh:
    async def test_refresh_without_cookie_returns_401(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.post("/refresh")
        assert resp.status_code == 401
