from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func

from .models import Review



class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_reviews(self):
        result = await self.db.scalars(
            select(Review).where(Review.is_active == True)
        )
        return result.all()

    async def get_reviews_by_product_id(self, product_id: int):
        result = await self.db.scalars(
            select(Review).where(
                Review.product_id == product_id,
                Review.is_active == True
            )
        )
        return result.all()

    async def create_review(self, user_id, review: dict):
        review_db = Review(user_id=user_id, **review)
        self.db.add(review_db)
        await self.db.commit()
        return review_db

    async def get_review_by_id(self, review_id: int):
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
