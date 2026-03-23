
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.models import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_categories(self, skip: int,  limit: int) -> list[Category]:
        categories_db = await self.db.scalars(select(Category).offset(skip).limit(limit))
        categories = categories_db.all()
        return categories


    async def get_one_category(self, category_id: int) -> Category | None:
        category_db = await self.db.scalars(select(Category).where(Category.id == category_id))
        category = category_db.first()
        return category


    async def update_category(self, category_id: int, category: dict):

        await self.db.execute(update(Category).where(Category.id == category_id).values(**category))
        await self.db.commit()
        return True

    async def delete_category_by_id(self, category_id: int):

        await self.db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
        await self.db.commit()
        return True


    async def create_category(self, name: str, parent_id: int | None) -> Category:

        category_create = Category(name = name, parent_id = parent_id)
        self.db.add(category_create)
        await self.db.commit()
        await self.db.refresh(category_create)
        return category_create

    async def get_category_by_name(self, name: str) -> Category | None:
        category_db = await self.db.scalars(select(Category).where(Category.name == name))
        category = category_db.first()
        return category