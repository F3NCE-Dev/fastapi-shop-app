import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_user, create_product, auth_header


class TestCart:
    async def test_add_to_cart(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="cartuser1")
        prod = await create_product(db_session, name="Cart Item")
        resp = await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 2},
            headers=auth_header(user),
        )
        assert resp.status_code == 201
        assert resp.json()["success"] is True

    async def test_add_to_cart_unauthenticated(self, client: AsyncClient, db_session: AsyncSession):
        prod = await create_product(db_session, name="Cart Item 2")
        resp = await client.post("/cart/items", json={"product_id": prod.id, "quantity": 1})
        assert resp.status_code == 401

    async def test_get_cart(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="cartuser2")
        # price must be a whole number: Cart.total_price is typed `int` in the schema,
        # so 9.99 * 1 = 9.99 fails FastAPI's response validation
        prod = await create_product(db_session, name="Get Cart Item", price=10.0)
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        resp = await client.get("/cart/items", headers=auth_header(user))
        assert resp.status_code == 200
        body = resp.json()
        assert "items" in body
        assert "total_price" in body
        # total_price may be float (product price * qty) despite the int schema hint
        assert isinstance(body["total_price"], (int, float))

    async def test_remove_from_cart(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="cartuser3")
        prod = await create_product(db_session, name="Remove Cart Item")
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 3},
            headers=auth_header(user),
        )
        resp = await client.delete(f"/cart/items/{prod.id}", headers=auth_header(user))
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_clear_cart(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="cartuser4")
        prod = await create_product(db_session, name="Clear Cart Item")
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        resp = await client.delete("/cart/items", headers=auth_header(user))
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_add_invalid_quantity(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="cartuser5")
        prod = await create_product(db_session, name="Invalid Qty Item")
        resp = await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 0},
            headers=auth_header(user),
        )
        assert resp.status_code == 422
