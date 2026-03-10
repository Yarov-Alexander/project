from fastapi import HTTPException, status

from .repositories import CategoryRepositories
from .schemas import CategoryCreate
from .models import Category


class CategoryServices:
    def __init__(self, category_repo: CategoryRepositories):
        self.category_repo = category_repo

    async def get_all_categories(self, skip: int=0, limit: int=100) -> list[Category]:
        all_categories = await self.category_repo.get_all_categories(skip=skip, limit=limit)
        return all_categories

    async def get_category_by_id(self, category_id: int):
        result = await self.category_repo.get_one_category(category_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return result


    async def update_category(self, category_id: int, category: CategoryCreate):
        category_db = await self.category_repo.get_one_category(category_id)

        if category_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        if category_db.parent_id is not None:
            parent = await self.category_repo.get_one_category(category_db.parent_id)
            if parent is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
            if parent.id == category_db.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category cannot be its own parent")

        result = await self.category_repo.update_category(category_id, **category.model_dump())
        return result


    async def create_category(self, category: CategoryCreate) -> Category:
        check = await self.category_repo.get_one_category(category.category_id)
        if check is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
        result = await self.category_repo.create_category(category.name, category.parent_id)
        return result


    async def delete_category(self, category_id: int):
        check = await self.category_repo.get_one_category(category_id)
        if check is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        result = await self.category_repo.delete_category_by_id(category_id)
        return result