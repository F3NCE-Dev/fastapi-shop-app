from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.config import settings

from database import setup_database

from contextlib import asynccontextmanager

from routers import cart, admin, auth, profile, order, product, oauth

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
app.include_router(product.router)
app.include_router(profile.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)
app.include_router(oauth.router)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
