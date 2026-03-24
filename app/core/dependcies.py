from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.modules.CartItem.repositories import CartRepository


# ==========================================
# Репозитории
# ==========================================
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

def get_cart_repository(db: AsyncSession = Depends(get_async_db)):
    from app.modules.CartItem.repositories import CartRepository
    return CartRepository(db)

# ==========================================
# Сервисы
# ==========================================
def get_category_service(
    category_repo: "CategoryRepository" = Depends(get_category_repository)
) -> "CategoryService":
    """Возвращает CategoryService."""
    from app.modules.categories.services import CategoryService
    return CategoryService(category_repo)


def get_product_service(
    product_repo: "ProductRepository" = Depends(get_product_repository)
) -> "ProductService":
    """Возвращает ProductService."""
    from app.modules.products.services import ProductService
    return ProductService(product_repo)


def get_user_service(
        user_repo: "UserRepository" = Depends(get_user_repository)
) -> "UserService":
    """Возвращает UserService."""
    from app.modules.users.services import UserService
    return UserService(user_repo)

def get_cart_service(cart_repo: CartRepository = Depends(get_cart_repository)) -> "CartService":
    from app.modules.CartItem.services import CartService
    return CartService(cart_repo)