from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from models.category import CategoryORM
from database import Base
from typing import Optional

class ProductORM(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True, on_delete="SET NULL")
    category: Mapped["CategoryORM"] = relationship(back_populates="products")
    image_url: Mapped[Optional[str]] = mapped_column(nullable=False)
