from fastapi import HTTPException, status

from .repositories import ReviewRepository
from .models import Review


class ReviewService:
    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    async def get_all_reviews(self):
        return await self.repo.get_all_active()

    async def get_product_reviews(self, product_id: int, product):
        if not product or not product.is_active:
            raise HTTPException(status_code=404, detail="Product not found")

        return await self.repo.get_by_product(product_id)

    async def create_review(self, data, user, product):
        if user.role != "buyer":
            raise HTTPException(status_code=403, detail="Only buyers can add reviews")

        if not product or not product.is_active:
            raise HTTPException(status_code=404, detail="Product not found")

        review = Review(
            user_id=user.id,
            product_id=data.product_id,
            comment=data.comment,
            grade=data.grade
        )

        review = await self.repo.create(review)

        # пересчёт рейтинга
        avg = await self.repo.calculate_avg_rating(data.product_id)
        await self.repo.update_product_rating(data.product_id, avg)

        return review

    async def delete_review(self, review_id: int, user):
        review = await self.repo.get_by_id(review_id)

        if not review or not review.is_active:
            raise HTTPException(status_code=404, detail="Review not found")

        if review.user_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")

        await self.repo.soft_delete(review)

        # пересчёт рейтинга
        avg = await self.repo.calculate_avg_rating(review.product_id)
        await self.repo.update_product_rating(review.product_id, avg)