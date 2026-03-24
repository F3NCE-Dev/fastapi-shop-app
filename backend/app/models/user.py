from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base, intpk, created_at, updated_at
from app.enums.roles import Role
from app.config.config import settings
from typing import Optional

class UserORM(Base):
    __tablename__ = "users"
    
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[Optional[str]] = mapped_column(unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=True, default=Role.user)
    profile_picture_url: Mapped[str] = mapped_column(nullable=True, default=settings.DEFAULT_PROFILE_PICTURE_URL)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
