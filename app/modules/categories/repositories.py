
from sqlalchemy import select, update, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.categories.models import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> Sequence[Category]:
        result = await self.db.scalars(select(Category).offset(skip).limit(limit))
        return result.all()


    async def get_one_category(self, category_id: int) -> Category | None:
        result = await self.db.scalars(select(Category).where(Category.id == category_id))
        return result.first()


    async def get_category_by_name(self, name: str) -> Category | None:
        result = await self.db.scalars(select(Category).where(Category.name == name))
        return result.first()


    async def create_category(self, name: str, parent_id: int | None) -> Category:
        category = Category(name=name, parent_id=parent_id)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category


    async def update_category(self, category_id: int, name: str, parent_id: int) -> Category:
        await self.db.execute(update(Category).where(Category.id == category_id).values(name=name, parent_id=parent_id))
        await self.db.commit()
        return await self.get_one_category(category_id)


    async def delete_category_by_id(self, category_id: int) -> None:
        await self.db.execute(update(Category).where(Category.id == category_id).values(is_active=False))
        await self.db.commit()
