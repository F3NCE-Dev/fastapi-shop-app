import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_category, create_product


class TestGetProducts:
    async def test_list_products_empty_or_more(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/products")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_list_products_returns_created(self, client: AsyncClient, db_session: AsyncSession):
        cat = await create_category(db_session, name="Gadgets")
        prod = await create_product(db_session, name="UniqueGadgetXYZ123", category_id=cat.id)
        # Use search so the default limit=10 doesn't hide the product when the DB
        # has accumulated many rows from other tests running in the same session
        resp = await client.get("/products?search=UniqueGadgetXYZ123")
        assert resp.status_code == 200
        ids = [p["id"] for p in resp.json()]
        assert prod.id in ids

    async def test_get_product_by_id(self, client: AsyncClient, db_session: AsyncSession):
        prod = await create_product(db_session, name="Solo Product")
        resp = await client.get(f"/products/{prod.id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Solo Product"

    async def test_get_product_not_found(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/products/999999")
        assert resp.status_code == 404

    async def test_filter_products_by_category(self, client: AsyncClient, db_session: AsyncSession):
        cat = await create_category(db_session, name="FilterCat")
        filtered = await create_product(db_session, name="FilteredProduct", category_id=cat.id)
        unfiltered = await create_product(db_session, name="UnfilteredProduct", category_id=None)
        resp = await client.get(f"/products?category_id={cat.id}")
        assert resp.status_code == 200
        ids = [p["id"] for p in resp.json()]
        assert filtered.id in ids
        assert unfiltered.id not in ids

    async def test_search_products_by_name(self, client: AsyncClient, db_session: AsyncSession):
        prod = await create_product(db_session, name="UniqueSearchTerm999")
        resp = await client.get("/products?search=UniqueSearchTerm999")
        assert resp.status_code == 200
        ids = [p["id"] for p in resp.json()]
        assert prod.id in ids

    async def test_products_pagination(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/products?limit=2&offset=0")
        assert resp.status_code == 200
        assert len(resp.json()) <= 2

    async def test_products_invalid_limit(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/products?limit=0")
        assert resp.status_code == 422
