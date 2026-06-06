import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_user, create_product, auth_header


class TestOrders:
    async def test_create_order_from_cart(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="orderuser1")
        prod = await create_product(db_session, name="Order Product", price=15.0)
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        resp = await client.post("/orders", headers=auth_header(user))
        assert resp.status_code == 201
        assert resp.json()["success"] is True

    async def test_get_orders_after_creating_one(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="orderuser2")
        prod = await create_product(db_session, name="Order Product 2", price=10.0)
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        await client.post("/orders", headers=auth_header(user))
        # get_orders raises 404 on empty list — always create an order first
        resp = await client.get("/orders", headers=auth_header(user))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert len(resp.json()) >= 1

    async def test_delete_order(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="orderuser3")
        prod = await create_product(db_session, name="Delete Order Product", price=5.0)
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        create_resp = await client.post("/orders", headers=auth_header(user))
        assert create_resp.status_code == 201
        # detail format: "Order 3 set successfully"
        order_id = int(create_resp.json()["detail"].split()[1])
        del_resp = await client.delete(f"/orders/{order_id}", headers=auth_header(user))
        assert del_resp.status_code == 200
        assert del_resp.json()["success"] is True

    async def test_orders_require_auth(self, client: AsyncClient, db_session: AsyncSession):
        resp = await client.get("/orders")
        assert resp.status_code == 401

    async def test_delete_nonexistent_order(self, client: AsyncClient, db_session: AsyncSession):
        user = await create_user(db_session, username="orderuser4")
        resp = await client.delete("/orders/999999", headers=auth_header(user))
        assert resp.status_code == 404
