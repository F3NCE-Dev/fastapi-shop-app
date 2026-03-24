from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.models.category import CategoryORM
from app.database import Base, intpk, created_at, updated_at
from typing import Optional

class ProductORM(Base):
    __tablename__ = "products"
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    category: Mapped["CategoryORM"] = relationship(back_populates="products")
    image_url: Mapped[Optional[str]] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
