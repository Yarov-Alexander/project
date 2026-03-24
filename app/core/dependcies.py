from .database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.modules.categories.repositories import CategoryRepository
from app.modules.categories.services import CategoryService
from app.modules.products.services import ProductService
from app.modules.products.repositories import ProductRepository
from ..modules.CartItem.repositories import CartRepository
from ..modules.CartItem.services import CartService
from ..modules.users.repositories import UserRepository
from ..modules.users.services import UserService


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db

def get_category_repository(db: AsyncSession = Depends(get_async_db)) -> CategoryRepository:
    return CategoryRepository(db=db)

def get_category_service(category_repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(category_repo=category_repo)
#----------------
def get_product_repository(db: AsyncSession = Depends(get_async_db)):
    return ProductRepository(db=db)

def get_product_service(product_repo: ProductRepository = Depends(get_product_repository),
                        category_repo: CategoryRepository = Depends(get_category_repository)):
    return ProductService(product_repo=product_repo, category_repo=category_repo)
#----------------
def get_user_repository(db: AsyncSession = Depends(get_async_db)):
    return UserRepository(db=db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo=user_repo)
#----------------
def get_cart_repository(db: AsyncSession = Depends(get_async_db)):
    return CartRepository(db=db)

def get_cart_service(cart_repo: CartRepository = Depends(get_cart_repository)):
    return CartService(cart_repo=cart_repo)