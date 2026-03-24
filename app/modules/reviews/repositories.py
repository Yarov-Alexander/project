from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func

from .models import Review
from app.modules.products.models import Product


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_active(self):
        result = await self.db.scalars(
            select(Review).where(Review.is_active == True)
        )
        return result.all()

    async def get_by_product(self, product_id: int):
        result = await self.db.scalars(
            select(Review).where(
                Review.product_id == product_id,
                Review.is_active == True
            )
        )
        return result.all()

    async def create(self, review: Review):
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_by_id(self, review_id: int):
        return await self.db.get(Review, review_id)

    async def soft_delete(self, review: Review):
        review.is_active = False
        await self.db.commit()

    async def calculate_avg_rating(self, product_id: int):
        result = await self.db.execute(
            select(func.avg(Review.grade)).where(
                Review.product_id == product_id,
                Review.is_active == True
            )
        )
        return result.scalar() or 0.0

    async def update_product_rating(self, product_id: int, rating: float):
        product = await self.db.get(Product, product_id)
        product.rating = rating
        await self.db.commit()