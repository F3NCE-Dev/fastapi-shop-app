import io
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import create_user, create_product, create_category, auth_header
from app.enums.roles import Role


class TestAdmin:
    async def test_admin_endpoints_require_admin_role(self, client: AsyncClient, db_session: AsyncSession):
        regular_user = await create_user(db_session, username="regularadmintest", role=Role.user)
        resp = await client.get("/admin/users", headers=auth_header(regular_user))
        assert resp.status_code == 403

    async def test_admin_get_users(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="admingetusers", role=Role.admin)
        resp = await client.get("/admin/users", headers=auth_header(admin))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_admin_get_user_by_id(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="admingetuserbyid", role=Role.admin)
        target = await create_user(db_session, username="targetuser")
        resp = await client.get(f"/admin/users/{target.id}", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["id"] == target.id

    async def test_admin_get_nonexistent_user(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminnotfound", role=Role.admin)
        resp = await client.get("/admin/users/999999", headers=auth_header(admin))
        assert resp.status_code == 404

    async def test_admin_add_category(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminaddcat", role=Role.admin)
        resp = await client.post(
            "/admin/categories",
            json={"name": "Admin Category"},
            headers=auth_header(admin),
        )
        assert resp.status_code == 201
        assert resp.json()["success"] is True

    async def test_admin_delete_category(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="admindelcat", role=Role.admin)
        cat = await create_category(db_session, name="ToDelete")
        resp = await client.delete(f"/admin/categories/{cat.id}", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_admin_get_all_orders(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminorders", role=Role.admin)
        user = await create_user(db_session, username="adminordercreator")
        prod = await create_product(db_session, name="Admin Orders Product", price=5.0)
        # admin get_all_orders raises 404 when empty — create one first
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        await client.post("/orders", headers=auth_header(user))
        resp = await client.get("/admin/orders", headers=auth_header(admin))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
        assert len(resp.json()) >= 1

    async def test_admin_update_order_status(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminupdorder", role=Role.admin)
        user = await create_user(db_session, username="ordercreatoradm")
        prod = await create_product(db_session, name="Admin Order Product", price=20.0)
        await client.post(
            "/cart/items",
            json={"product_id": prod.id, "quantity": 1},
            headers=auth_header(user),
        )
        create_resp = await client.post("/orders", headers=auth_header(user))
        order_id = int(create_resp.json()["detail"].split()[1])
        resp = await client.patch(
            f"/admin/orders/{order_id}?status=shipped",
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_admin_update_user_role(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminrolechange", role=Role.admin)
        target = await create_user(db_session, username="rolechangetarget")
        resp = await client.patch(
            f"/admin/users/{target.id}?role=admin",
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_admin_add_product(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminaddprod", role=Role.admin)
        fake_image = io.BytesIO(b"fake image content")
        resp = await client.post(
            "/admin/products",
            data={"name": "Admin Product", "price": "29.99"},
            files={"image": ("test.jpg", fake_image, "image/jpeg")},
            headers=auth_header(admin),
        )
        assert resp.status_code == 201
        assert resp.json()["success"] is True

    async def test_admin_delete_product(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="admindelprod", role=Role.admin)
        prod = await create_product(db_session, name="To Be Deleted")
        resp = await client.delete(f"/admin/products/{prod.id}", headers=auth_header(admin))
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_admin_users_pagination(self, client: AsyncClient, db_session: AsyncSession):
        admin = await create_user(db_session, username="adminpaginator", role=Role.admin)
        resp = await client.get("/admin/users?limit=2&offset=0", headers=auth_header(admin))
        assert resp.status_code == 200
        assert len(resp.json()) <= 2
