from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base

class CategoryORM(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    products: Mapped[list["ProductORM"]] = relationship(back_populates="category", cascade="save-update")
