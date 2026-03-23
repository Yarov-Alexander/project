from fastapi import APIRouter, Depends, status, HTTPException

from .exceptions import ProductNotFound
from .schemas import Product as ProductSchema, ProductCreate
from app.core.dependcies import get_product_repository, get_product_service
from .services import ProductService
from ..categories.exceptions import CategoryNotFound

router = APIRouter(prefix="/products",
                   tags=["products"]
                   )

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)):
    try:
        result = await product_service.get_product_by_id(product_id=product_id)
        return result
    except ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, product_service: ProductService = Depends(get_product_service)) -> ProductSchema:
    try:
        result = await product_service.create_product(product=product)
        return result
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")