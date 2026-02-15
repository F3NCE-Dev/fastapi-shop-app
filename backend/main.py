from fastapi import FastAPI

from database import setup_database

from contextlib import asynccontextmanager

from routers import cart, profile_edit, admin, auth, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(profile_edit.router)
app.include_router(admin.router)
