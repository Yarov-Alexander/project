from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint





class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column('quantity >= 0', nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="cart_items")
    products: Mapped["Product"] = relationship("Product", back_populates="cart_items")

    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='user_id_product_id_unique'),)
