
from .repositories import ProductRepository
from app.modules.categories.repositories import CategoryRepository

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

    async def create_product(self, seller_id: int, product_dict: dict):

        category = await self.category_repo.get_one_category(product_dict["category_id"])  # Добавить Пользователя !!
        if not category:
            raise CategoryNotFound()

        result = await self.product_repo.create_product(seller_id=seller_id, product=product_dict)
        return result

    async def update_product(self, seller_id: int, product_dict: dict, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFound()
        if product.seller_id != seller_id:
            raise ValueError()

        category = await self.category_repo.get_one_category(product.category_id)
        if not category:
            raise CategoryNotFound()

        product = await self.product_repo.update_product(product_dict=product_dict, product_id=product_id)
        return product

    async def delete_product(self, product_id: int, user_id: int):
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            raise ProductNotFound()
        if product.category_id != user_id:
            raise ValueError()
        await self.product_repo.delete_product(product_id=product_id, user_id=user_id)
