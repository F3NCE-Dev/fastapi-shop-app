from sqlalchemy.orm import mapped_column, Mapped
from database import Base

class ProductORM(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)
