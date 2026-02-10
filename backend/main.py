from fastapi import FastAPI

from database import setup_database

from contextlib import asynccontextmanager

from routers import AdminRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(AdminRouter.router)
