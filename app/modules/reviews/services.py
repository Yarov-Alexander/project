from fastapi import Depends

from .repositories import ReviewRepository
from ..products.exceptions import ProductNotFound
from ..products.repositories import ProductRepository
from ..users.models import User
from ...core.exceptions import ReviewNotFound


class ReviewService:
    def __init__(self, review_repo: ReviewRepository, product_repo: ProductRepository):
        self.review_repo = review_repo
        self.product_repo = product_repo

    async def get_all_reviews(self):
        return await self.review_repo.get_all_reviews()


    async def get_reviews_by_product_id(self, product_id: int):

        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFound()
        reviews =  await self.review_repo.get_reviews_by_product_id(product_id)
        if not reviews:
            raise ReviewNotFound()
        return reviews


    async def create_review(self, data: dict):

        product = await self.product_repo.get_product_by_id(data["product_id"])
        if not product:
            raise ProductNotFound()
        review = await self.review_repo.create_review(data)


        avg = await self.review_repo.calculate_avg_rating(data["product_id"])
        await self.product_repo.update_product_rating(data["product_id"], avg)

        return await self.review_repo.get_reviews_by_product_id(review.product_id)


    async def delete_review(self, review_id: int):
        review = await self.review_repo.get_review_by_id(review_id)

        if not review or not review.is_active:
            raise ReviewNotFound()

        await self.review_repo.soft_delete(review)

        avg = await self.review_repo.calculate_avg_rating(review.product_id)
        await self.product_repo.update_product_rating(review.product_id, avg)