from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from config.config import settings

engine = create_async_engine(settings.DATABASE_URL)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class ProductORM(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

async def get_db():
    async with new_session() as session:
        yield session

async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
