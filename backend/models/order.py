from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from database import Base

class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    total_price: Mapped[int] = mapped_column(nullable=False, default=0)

    items: Mapped[list["OrderItemORM"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItemORM(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_purchase: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["OrderORM"] = relationship(back_populates="items")
