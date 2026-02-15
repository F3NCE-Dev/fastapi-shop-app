from fastapi import FastAPI

from database import setup_database

from contextlib import asynccontextmanager

from routers import user_router, admin_router, auth_router, profile_edit_router, cart

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(cart.router)
app.include_router(profile_edit_router.router)
app.include_router(admin_router.router)
