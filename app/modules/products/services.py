from .repositories import ProductRepository
from app.modules.categories.repositories import CategoryRepository
from app.core.dependcies import  get_category_repository
from .schemas import ProductCreate
from .exceptions import ProductNotFound
from app.modules.categories.exceptions import CategoryNotFound


class ProductService:
    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository):
        self.product_repo = product_repo
        self.category_repo = category_repo


    async def get_product_by_id(self, product_id: int):
        result = await self.product_repo.get_product_by_id(product_id)

        if not result:
            raise ProductNotFound()

        return result


    async def create_product(self, product: ProductCreate):
        category = await self.category_repo.get_one_category(product.category_id)
                                                                                        # Добавить Пользователя !!
        if not category:
            raise CategoryNotFound()

        result = await self.product_repo.create_product(product=product)
        await self.product_repo.db.commit()
        await self.product_repo.db.refresh(result)
        return result



