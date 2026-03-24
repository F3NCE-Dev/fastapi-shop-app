from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.database import Base, intpk, created_at, updated_at
from app.enums.order_status import OrderStatus
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum

class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_price: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.pending)
    items: Mapped[list["OrderItemORM"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class OrderItemORM(Base):
    __tablename__ = "order_items"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_purchase: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["OrderORM"] = relationship(back_populates="items")
