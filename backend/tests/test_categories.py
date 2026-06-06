import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_category


class TestCategories:
    async def test_get_categories_empty(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/categories")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_get_categories_returns_created(self, client: AsyncClient, db_session: AsyncSession):
        await create_category(db_session, name="Books")
        resp = await client.get("/categories")
        assert resp.status_code == 200
        names = [c["name"] for c in resp.json()]
        assert "Books" in names
