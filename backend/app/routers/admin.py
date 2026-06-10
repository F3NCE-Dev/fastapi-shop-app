from fastapi import APIRouter, Depends, Query, UploadFile, File, Form

from app.repositories.admin import AdminCommands
from app.schemas.order import Order
from app.schemas.product import ProductBase, ProductUpdate
from app.schemas.responses import StatusResponse, AccessTokenResponse
from app.schemas.user import UserID
from app.schemas.category import CategoryBase
from app.enums.order_status import OrderStatus
from app.enums.roles import Role
from app.permissions.permissions import admin_required
from app.dependencies import DBSession, REDIS

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(admin_required)])

@router.post("/products", response_model=StatusResponse, status_code=201)
async def admin_add_product(
    db: DBSession,
    redis: REDIS,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    category_id: int = Form(None),
    image: UploadFile = File(...),
):
    data = ProductBase(name=name, description=description, price=price, category_id=category_id)

    product_id = await AdminCommands.add_product(
        data=data,
        image=image,
        db=db,
        redis=redis
    )

    return {"success": True, "detail": f"Product {product_id} added successfully"}

@router.delete("/products/{product_id}", response_model=StatusResponse)
async def admin_remove_product(product_id: int, db: DBSession, redis: REDIS):
    product_id = await AdminCommands.remove_product(product_id=product_id, db=db, redis=redis)
    return {"success": True, "detail": f"Product {product_id} removed successfully"}

@router.patch("/products/{product_id}", response_model=StatusResponse)
async def admin_update_product(
    db: DBSession,
    redis: REDIS,
    product_id: int,
    category_id: int | None = Form(None),
    name: str | None = Form(None),
    description: str | None = Form(None),
    price: float | None = Form(None),
    image: UploadFile | None = File(None)
):
    data = ProductUpdate(category_id=category_id, name=name, description=description, price=price)
    product_id = await AdminCommands.update_product(product_id=product_id, data=data, image=image, db=db, redis=redis)
    return {"success": True, "detail": f"Product {product_id} updated successfully"}

@router.post("/category", response_model=StatusResponse, status_code=201)
async def admin_add_category(data: CategoryBase, db: DBSession, redis: REDIS):
    category_id = await AdminCommands.add_category(data=data, db=db, redis=redis)
    return {"success": True, "detail": f"Category {category_id} added successfully"}

@router.delete("/category/{category_id}", response_model=StatusResponse)
async def admin_delete_category(category_id: int, db: DBSession, redis: REDIS):
    category_id = await AdminCommands.delete_category(category_id=category_id, db=db, redis=redis)
    return {"success": True, "detail": f"Category {category_id} deleted successfully"}

@router.patch("/orders/{order_id}", response_model=StatusResponse)
async def admin_update_order_status(
                                    db: DBSession,
                                    order_id: int,
                                    status: OrderStatus = Query(..., description="New status for the order")
                                    ):
    order_id = await AdminCommands.update_order_status(order_id=order_id, status=status, db=db)
    return {"success": True, "detail": f"Order {order_id} updated successfully"}

@router.get("/orders", response_model=list[Order])
async def get_orders(db: DBSession):
    return await AdminCommands.get_all_orders(db)

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int, db: DBSession):
    return await AdminCommands.get_order(order_id=order_id, db=db)

@router.patch("/users/{user_id}", response_model=AccessTokenResponse)
async def admin_update_user_role(
                                 db: DBSession,
                                 user_id: int,
                                 role: Role = Query(..., description="New role for the user")
                                 ):
    new_access_token = await AdminCommands.update_user_role(user_id=user_id, role=role, db=db)
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/users", response_model=list[UserID])
async def get_users(db: DBSession,
                    limit: int = Query(10, ge=1, le=100),
                    offset: int = Query(0, ge=0)
                    ):
    return await AdminCommands.get_all_users(limit=limit, offset=offset, db=db)

@router.get("/users/{user_id}", response_model=UserID)
async def get_user(user_id: int, db: DBSession):
    return await AdminCommands.get_user(user_id, db)
