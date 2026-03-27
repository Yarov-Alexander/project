
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.modules.products.repositories import ProductRepository
from app.modules.CartItem.models import CartItem as CartItemModel
from app.modules.products.models import Product


class CartRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_product_by_id(self, product_id: int):
        product_repo = ProductRepository(self.db)
        return await product_repo.get_product_by_id(product_id)


    async def get_cart_items(self, user_id: int):
        result = await self.db.scalars(
            select(CartItemModel)
            .options(selectinload(CartItemModel.product))
            .where(CartItemModel.user_id == user_id)
            .order_by(CartItemModel.id)
        )
        return result.all()


    async def get_cart_item(self, user_id: int, product_id: int):
        result = await self.db.scalars(
            select(CartItemModel)
            .options(selectinload(CartItemModel.product))
            .where(
                CartItemModel.user_id == user_id,
                CartItemModel.product_id == product_id
            )
        )
        return result.first()


    async def delete_cart_item(self, cart_item: CartItemModel):
        await self.db.delete(cart_item)
        await self.db.commit()


    async def clear_cart(self, user_id: int):
        await self.db.execute(
            delete(CartItemModel).where(CartItemModel.user_id == user_id)
        )
        await self.db.commit()

    async def add_cart_item(self, cart_item: CartItemModel):
        self.db.add(cart_item)
        await self.db.commit()
