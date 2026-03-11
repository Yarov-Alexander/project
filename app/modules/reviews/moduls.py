from sqlalchemy import ForeignKey, DateTime, CheckConstraint
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from decimal import Decimal

class ReviewModel(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment: Mapped[str|None] = mapped_column(nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)
    grade: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=True, default=True)
    rating: Mapped[float] = mapped_column(default=0.0)

    products = relationship("Product", back_populates="reviews_products")
    users = relationship("User", back_populates="reviews_users")

    __table_args__ = (
        CheckConstraint("grade >= 1 AND grade <= 5", name="grade_greater_5"),
    )