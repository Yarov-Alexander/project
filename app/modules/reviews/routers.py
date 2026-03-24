from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.dependcies import get_async_db
from .schemas import ReviewCreate, ReviewResponse
from .repositories import ReviewRepository
from .services import ReviewService

from app.modules.products.repositories import ProductRepository
from app.auth.dependcies import get_current_user


router = APIRouter(prefix="/reviews", tags=["Reviews"])


def get_review_service(db: AsyncSession = Depends(get_async_db)):
    return ReviewService(ReviewRepository(db))


def get_product_repo(db: AsyncSession = Depends(get_async_db)):
    return ProductRepository(db)


# GET /reviews/
@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(service: ReviewService = Depends(get_review_service)):
    return await service.get_all_reviews()


# GET /products/{product_id}/reviews/
@router.get("/products/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: int,
    service: ReviewService = Depends(get_review_service),
    product_repo: ProductRepository = Depends(get_product_repo),
):
    product = await product_repo.get_by_id(product_id)
    return await service.get_product_reviews(product_id, product)


# POST /reviews/
@router.post("/", response_model=ReviewResponse)
async def create_review(
    data: ReviewCreate,
    service: ReviewService = Depends(get_review_service),
    product_repo: ProductRepository = Depends(get_product_repo),
    user=Depends(get_current_user),
):
    product = await product_repo.get_by_id(data.product_id)
    return await service.create_review(data, user, product)


# DELETE /reviews/{review_id}
@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
    user=Depends(get_current_user),
):
    await service.delete_review(review_id, user)
    return {"message": "Review deleted"}