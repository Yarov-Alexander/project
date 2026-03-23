from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Product
from .schemas import ProductCreate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(self, product_id: int):
        result = await self.db.scalars(select(Product).where(Product.id == product_id))
        return result.one_or_none()

    async def create_product(self, product: ProductCreate):
        product_db = Product(**product.model_dump())
        self.db.add(product_db)

        return product_db
