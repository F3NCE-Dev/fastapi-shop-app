from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.config import settings

from app.database import setup_database

from app.routers import cart, admin, auth, profile, order, product, oauth, category, user

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(profile.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)
app.include_router(oauth.router)

app.mount("/static", StaticFiles(directory=settings.STATIC_FOLDER), name="static")
