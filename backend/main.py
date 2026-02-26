from fastapi import FastAPI

from database import setup_database

from contextlib import asynccontextmanager

from routers import cart, admin, auth, user, profile, order

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)
