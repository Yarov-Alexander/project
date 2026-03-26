from fastapi import APIRouter, Depends, status, HTTPException, Response

from .exceptions import ProductNotFound
from .schemas import Product as ProductSchema, ProductCreate
from app.core.dependcies import  get_product_service
from .services import ProductService
from ..categories.exceptions import CategoryNotFound
from ..users.models import User
from ...auth.dependcies import get_current_seller


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
async def create_product(product: ProductCreate,
                         product_service: ProductService = Depends(get_product_service),
                         current_user: User = Depends(get_current_seller)
                         ) -> ProductSchema:
    try:
        result = await product_service.create_product(product.model_dump(), seller_id=current_user.id)
        return result
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
        product_id: int,
        product: ProductCreate,
        product_service: ProductService = Depends(get_product_service),
        current_user: User = Depends(get_current_seller),
) -> ProductSchema:
    try:
        product = await product_service.update_product(seller_id=current_user.id, product_id=product_id, product_dict=product.model_dump())
    except ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int,
                         current_user: User = Depends(get_current_seller),
                         product_service: ProductService = Depends(get_product_service)):
    try:
        await product_service.delete_product(product_id=product_id, user_id=current_user.id)
    except ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own products")
    return Response(status_code=status.HTTP_204_NO_CONTENT)