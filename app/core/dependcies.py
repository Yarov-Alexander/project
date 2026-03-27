from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.modules.CartItem.repositories import CartRepository
from app.modules.categories.repositories import CategoryRepository
from app.modules.products.repositories import ProductRepository
from app.modules.reviews.repositories import ReviewRepository
from app.modules.users.repositories import UserRepository


# ---- Репозитории

def get_category_repository(
    db: AsyncSession = Depends(get_async_db)
) -> "CategoryRepository":
    """Возвращает CategoryRepository."""
    from app.modules.categories.repositories import CategoryRepository
    return CategoryRepository(db)


def get_product_repository(
    db: AsyncSession = Depends(get_async_db)
) -> "ProductRepository":
    """Возвращает ProductRepository."""
    from app.modules.products.repositories import ProductRepository
    return ProductRepository(db)


def get_user_repository(
    db: AsyncSession = Depends(get_async_db)
) -> "UserRepository":
    """Возвращает UserRepository."""
    from app.modules.users.repositories import UserRepository
    return UserRepository(db)

def get_cart_repository(
    db: AsyncSession = Depends(get_async_db)
) -> "CartRepository":
    """Возвращает CartRepository."""
    from app.modules.CartItem.repositories import CartRepository
    return CartRepository(db)

def get_review_repository(db: AsyncSession = Depends(get_async_db)) -> "ReviewRepository":
    from app.modules.reviews.repositories import ReviewRepository
    return ReviewRepository(db)




# ----- Сервисы

def get_category_service(db: AsyncSession = Depends(get_async_db)) -> "CategoryService":
    """Возвращает CategoryService."""
    from app.modules.categories.services import CategoryService
    return CategoryService(category_repo=CategoryRepository(db))


def get_product_service(db: AsyncSession = Depends(get_async_db)) -> "ProductService":
    """Возвращает ProductService."""
    from app.modules.products.services import ProductService
    return ProductService(
        product_repo=ProductRepository(db),
        category_repo=CategoryRepository(db)
    )


def get_user_service(db: AsyncSession = Depends(get_async_db)) -> "UserService":
    """Возвращает UserService."""
    from app.modules.users.services import UserService
    return UserService(user_repo=UserRepository(db))


def get_cart_service(db: AsyncSession = Depends(get_async_db)) -> "CartService":
    from app.modules.CartItem.services import CartService

    return CartService(
        cart_repo=CartRepository(db),
        product_repo=ProductRepository(db)
    )


def get_review_service(db: AsyncSession = Depends(get_async_db)) -> "ReviewService":
    from app.modules.reviews.services import ReviewService
    return ReviewService(review_repo=ReviewRepository(db), product_repo=ProductRepository(db))