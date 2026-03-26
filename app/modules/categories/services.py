from fastapi import HTTPException, status

from .exceptions import CategoryAlreadyExists
from .repositories import CategoryRepository

from .models import Category
from ...core.exceptions import NotFound, BadRequest


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo


    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> list[Category]:
        return await self.category_repo.get_all_categories(skip=skip, limit=limit)


    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.category_repo.get_one_category(category_id)
        if not category:
            raise NotFound("Category not found")
        return category


    async def create_category(self, name: str, parent_id: int) -> Category:
        # Проверяем уникальность имени
        existing = await self.category_repo.get_category_by_name(name)
        if existing:
            raise CategoryAlreadyExists()

        return await self.category_repo.create_category(name, parent_id)


    async def update_category(self, category_id: int, name: str, parent_id: int) -> Category:
        category_db = await self.category_repo.get_one_category(category_id)
        if not category_db:
            raise NotFound("Category not found")

        # Проверка на то, чтобы родитель не был самим собой
        if parent_id is not None and parent_id == category_id:
            raise BadRequest("Parent cannot be the same as category")
        return await self.category_repo.update_category(category_id, name, parent_id)


    async def delete_category(self, category_id: int) -> None:
        category_db = await self.category_repo.get_one_category(category_id)
        if not category_db:
            raise NotFound("Category not found")
        await self.category_repo.delete_category_by_id(category_id)