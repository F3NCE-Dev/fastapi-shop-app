from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.database import Base, intpk, created_at, updated_at

class CartORM(Base):
    __tablename__ = "carts"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    items: Mapped[list["CartItemORM"]] = relationship(back_populates="cart", cascade="all, delete-orphan")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class CartItemORM(Base):
    __tablename__ = "cart_items"
    id: Mapped[intpk]
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)

    cart: Mapped["CartORM"] = relationship(back_populates="items")
