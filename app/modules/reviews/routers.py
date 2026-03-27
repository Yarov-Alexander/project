from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List

from .schemas import ReviewCreate, ReviewResponse
from app.core.dependcies import get_review_service
from .services import ReviewService

from app.auth.dependcies import get_current_user, get_current_buyer
from ..products.exceptions import ProductNotFound
from ..users.models import User
from ...core.exceptions import ReviewNotFound

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(review_service: ReviewService = Depends(get_review_service)) -> List[ReviewResponse]:
    return await review_service.get_all_reviews()


@router.get("/products/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(
    product_id: int,
    service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_user),
) -> List[ReviewResponse]:
    try:
        return await service.get_reviews_by_product_id(product_id)
    except ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except ReviewNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_create: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_buyer),
):
    try:
        return await review_service.create_review(review_create.model_dump())
    except ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
    user=Depends(get_current_user),
):
    try:
        await service.delete_review(review_id, user)
    except ReviewNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)