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
            return None
        return result


    async def update_category(self, category_id: int, category: CategoryCreate):
        check = await self.category_repo.get_one_category(category_id)
        if check is None:
            return None
        result = await self.category_repo.update_category(category_id, **category.model_dump())
        return result

    async def create_category(self, category: CategoryCreate):
        check = await self.category_repo.get_one_category(category.category_id)
        if check is not None:
            return None
        result = await self.category_repo.create_category(category.name, category.parent_id)
        return result

    async def delete_category(self, category_id: int):
        check = await self.category_repo.get_one_category(category_id)
        if check is None:
            return None
        result = await self.category_repo.delete_category_by_id(category_id)
        return result