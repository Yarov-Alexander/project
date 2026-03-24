from fastapi import APIRouter, status, Depends
from .services import CategoryService
from .schemas import Category as CategorySchema, CategoryCreate
from app.core.dependcies import get_category_service

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(service: CategoryService = Depends(get_category_service)):
    return await service.get_all_categories()

@router.get("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(category_id: int, service: CategoryService = Depends(get_category_service)):
    return await service.get_category_by_id(category_id)

@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return await service.create_category(category)

@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int, category: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    return await service.update_category(category_id, category)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    await service.delete_category(category_id)
    return {"message": f"Category with ID {category_id} deleted"}

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