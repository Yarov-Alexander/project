from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import Product



class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(self, product_id: int):
        result = await self.db.scalars(select(Product).where(Product.id == product_id))
        return result.one_or_none()

    async def create_product(self,seller_id: int, product: dict):
        product_db = Product(seller_id, **product)
        self.db.add(product_db)
        await self.db.commit()

        return await self.db.refresh(product_db)


    async def update_product(self, product_dict: dict, product_id: int):
        await self.db.scalars(update(Product).where(Product.id == product_id).values(**product_dict))
        await self.db.commit()
        product_db = await self.db.scalars(select(Product).where(Product.id == product_id))
        return product_db.first()

    async def delete_product(self, product_id: int, user_id: int):
        await self.db.execute(update(Product).where(Product.id == product_id, user_id=user_id).values(is_active=False))
        await self.db.commit()

    async def update_product_rating(self, product_id: int, rating: Decimal):
        product = await self.db.get(Product, product_id)
        product.rating = rating
        await self.db.commit()