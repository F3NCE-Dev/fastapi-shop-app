from sqlalchemy.orm import mapped_column, Mapped
from database import Base
from enums.roles import Role

from config.config import settings

class UserORM(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=True, default=Role.USER)
    profile_picture_url: Mapped[str] = mapped_column(nullable=True, default=settings.DEFAULT_PROFILE_PICTURE_URL)
