from fastapi import HTTPException, status
from .repositories import CategoryRepository
from .schemas import CategoryCreate
from .models import Category


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> list[Category]:
        return await self.category_repo.get_all_categories(skip=skip, limit=limit)

    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.category_repo.get_one_category(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    async def create_category(self, category: CategoryCreate) -> Category:
        # Проверяем уникальность имени
        existing = await self.category_repo.get_category_by_name(category.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
        return await self.category_repo.create_category(category.name, category.parent_id)

    async def update_category(self, category_id: int, category: CategoryCreate) -> Category:
        category_db = await self.category_repo.get_one_category(category_id)
        if not category_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        # Проверка на то, чтобы родитель не был самим собой
        if category.parent_id is not None and category.parent_id == category_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Category cannot be its own parent")
        return await self.category_repo.update_category(category_id, category.model_dump())

    async def delete_category(self, category_id: int) -> None:
        category_db = await self.category_repo.get_one_category(category_id)
        if not category_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        await self.category_repo.delete_category_by_id(category_id)