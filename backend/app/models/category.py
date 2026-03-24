from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base, intpk, created_at, updated_at

class CategoryORM(Base):
    __tablename__ = "categories"
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    products: Mapped[list["ProductORM"]] = relationship(back_populates="category", cascade="save-update")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
