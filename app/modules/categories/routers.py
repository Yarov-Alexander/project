from fastapi import APIRouter, status, HTTPException, Depends
from .services import CategoryService

from app.core.dependcies import get_category_service
from .schemas import Category as CategorySchema, CategoryCreate
from .models import Category as CategoryModel

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/{category_id}", response_model=CategoryModel)
async def get_category_by_id(category_id: int, category_service: CategoryService = Depends(get_category_service)):
    result = await category_service.get_category_by_id(category_id)
    return result

@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategoryModel]:
    """
    Возвращает список всех категорий товаров.
    """
    result = await category_service.get_all_categories()
    return result


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category_body: CategoryCreate, category_service: CategoryService = Depends(get_category_service)) -> CategoryModel:
    """
    Создаёт новую категорию.
    """
    result = await category_service.create_category(category = category_body)
    return result


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int, category: CategoryCreate,
                          category_service: CategoryService = Depends(get_category_service)) -> CategoryModel:
    """
    Обновляет категорию по её ID.
    """
    result = await category_service.update_category(category_id, category)
    return result


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, category_service: CategoryService = Depends(get_category_service)) -> dict:
    """
    Удаляет категорию по её ID.
    """

    await category_service.delete_category(category_id)
    return {"message": f"Категория с ID {category_id} удалена"}