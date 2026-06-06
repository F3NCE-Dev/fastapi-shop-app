import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# ── patch settings before importing anything from app ────────────────────────
import app.config.config as _cfg
_cfg.settings.DATABASE_URL = "sqlite+aiosqlite:///:memory:"
_cfg.settings.SECRET_KEY = "test-secret-key"
_cfg.settings.STATIC_FOLDER = "static"
_cfg.settings.PROFILE_PICTURES_PATH = "static/profile_pictures"
_cfg.settings.DEFAULT_PROFILE_PICTURE_URL = "static/default_profile_pic/default.png"
_cfg.settings.PRODUCT_IMAGES_PATH = "static/product_images"

from app.main import app
from app.database import Base, get_db
from app.auth.security import create_access_token, hash_password
from app.models.user import UserORM
from app.models.product import ProductORM
from app.models.category import CategoryORM
from app.models.cart import CartORM, CartItemORM
from app.enums.roles import Role

# ── engine shared for the whole session ──────────────────────────────────────
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    """Create all tables once, drop them after the session ends."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    """Each test gets its own session that is rolled back on teardown."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(autouse=True)
async def override_get_db(db_session: AsyncSession):
    """Replace FastAPI's DB dependency with the test session."""
    async def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


# ── DB helpers (imported by test modules) ────────────────────────────────────

async def create_user(
    db: AsyncSession,
    username: str = "testuser",
    password: str = "secret123",
    role: Role = Role.user,
) -> UserORM:
    user = UserORM(
        username=username,
        hashed_password=hash_password(password),
        role=role,
        profile_picture_url="static/default_profile_pic/default.png",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def auth_header(user: UserORM) -> dict:
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}


async def create_category(db: AsyncSession, name: str = "Electronics") -> CategoryORM:
    cat = CategoryORM(name=name)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def create_product(
    db: AsyncSession,
    name: str = "Widget",
    price: float = 10.0,  # whole number so Cart.total_price (int schema) coerces cleanly
    category_id: int | None = None,
) -> ProductORM:
    prod = ProductORM(
        name=name,
        description="A fine widget",
        price=price,
        category_id=category_id,
        image_url="static/product_images/widget.png",
    )
    db.add(prod)
    await db.commit()
    await db.refresh(prod)
    return prod
