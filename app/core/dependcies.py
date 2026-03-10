from .database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.modules.categories.repositories import CategoryRepositories
from app.modules.categories.services import CategoryServices


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db

def get_category_repository(db: AsyncSession = Depends(get_async_db)) -> CategoryRepositories:
    return CategoryRepositories(db=db)

def get_category_service(category_repo: CategoryRepositories = Depends(get_category_repository)) -> CategoryServices:
    return CategoryServices(category_repo=category_repo)