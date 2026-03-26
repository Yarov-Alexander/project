from fastapi import APIRouter, status, Depends, HTTPException, Response

from .exceptions import CategoryAlreadyExists
from .services import CategoryService
from .schemas import Category as CategorySchema, CategoryCreate
from app.core.dependcies import get_category_service
from ...core.exceptions import NotFound, BadRequest

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(service: CategoryService = Depends(get_category_service)):
    return await service.get_all_categories()


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(category_id: int, service: CategoryService = Depends(get_category_service)):
    try:
        return await service.get_category_by_id(category_id)
    except NotFound("Category not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    try:
        return await service.create_category(**category.model_dump())
    except CategoryAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int, category: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    try:
        return await service.update_category(category_id, **category.model_dump())
    except NotFound("Category not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    except BadRequest:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    try:
        await service.delete_category(category_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NotFound("Category not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

