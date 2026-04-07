from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base, intpk, created_at
from datetime import datetime

class RefreshTokenORM(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[intpk]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    revoked: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[created_at]
    
    user = relationship("UserORM", backref="refresh_tokens")
