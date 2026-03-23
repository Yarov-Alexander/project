


from decimal import Decimal

from app.modules.CartItem.repositories import CartRepository


class CartService:

    def __init__(self, cart_repo: CartRepository):
        self.cart_repo = cart_repo

    
    async def _ensure_product_available(self, product_id: int):
        product = await self.cart_repo.get_product_by_id(product_id)

        if not product:
            return None

        return product


    async def get_user_cart_items(self, user_id: int):
        return await self.cart_repo.get_cart_items(user_id)


    async def _get_cart_item(self, user_id: int, product_id: int):
        return await self.cart_repo.get_cart_item(user_id, product_id)


    async def add_item(self, user_id: int, product_id: int, quantity: int):
        product = await self._ensure_product_available(product_id)

        if not product:
            raise ValueError("Product not found")

        cart_item = await self._get_cart_item(user_id, product_id)

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = await self.cart_repo.create_cart_item(
                user_id, product_id, quantity
            )

        await self.cart_repo.commit()

        return await self._get_cart_item(user_id, product_id)


    async def update_item(self, user_id: int, product_id: int, quantity: int):
        product = await self._ensure_product_available(product_id)

        if not product:
            raise ValueError("Product not found")

        cart_item = await self._get_cart_item(user_id, product_id)

        if not cart_item:
            raise ValueError("Cart item not found")

        cart_item.quantity = quantity

        await self.cart_repo.commit()

        return await self._get_cart_item(user_id, product_id)


    async def delete_item(self, user_id: int, product_id: int):
        cart_item = await self._get_cart_item(user_id, product_id)

        if not cart_item:
            raise ValueError("Cart item not found")

        await self.cart_repo.delete_cart_item(cart_item)
        await self.cart_repo.commit()


    async def clear_cart(self, user_id: int):
        await self.cart_repo.clear_cart(user_id)
        await self.cart_repo.commit()


    async def get_cart(self, user_id: int):
        items = await self.cart_repo.get_cart_items(user_id)

        total_quantity = sum(item.quantity for item in items)

        total_price = sum(
            Decimal(item.quantity) *
            (item.product.price if item.product.price else Decimal("0"))
            for item in items
        )

        return {
            "user_id": user_id,
            "items": items,
            "total_quantity": total_quantity,
            "total_price": total_price,
        }