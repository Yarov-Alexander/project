from decimal import Decimal

from app.core.exceptions import ProductNotFound, CartNotFound
from app.modules.CartItem.schemas import Cart
from app.modules.CartItem.repositories import CartRepository
from app.modules.CartItem.models import CartItem as CartItemModel
from app.modules.products.repositories import ProductRepository


class CartService:

    def __init__(self, cart_repo: CartRepository, product_repo: ProductRepository):
        self.cart_repo = cart_repo
        self.product_repo = product_repo
    
    async def _ensure_product_available(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id)
        if not product:
            return None
        return product


    async def _get_cart_item(self, user_id: int, product_id: int):
        return await self.cart_repo.get_cart_item(user_id, product_id)


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

    async def get_user_cart_items(self, user_id: int) -> Cart:
        items = await self.cart_repo.get_cart_items(user_id)
        total_quantity = sum(item.quantity for item in items)

        price_items = (
            Decimal(item.quantity) *
            (item.products.price if item.products.price is not None else Decimal("0"))
            for item in items
        )
        total_price_decimal = sum(price_items, Decimal("0.00"))

        return Cart(
            user_id=user_id,
            items=items,
            total_quantity=total_quantity,
            total_price=total_price_decimal,
        )


    async def add_item_to_cart(self, user_id: int, product_id: int, quantity: int):
        product = await self._ensure_product_available(product_id)
        if not product:
            raise ProductNotFound()
        cart_item = await self._get_cart_item(user_id, product_id)

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItemModel(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
        await self.cart_repo.add_cart_item(cart_item)

        return await self._get_cart_item(user_id, product_id)


    async def update_item(self, user_id: int, product_id: int, quantity: int):
        product = await self._ensure_product_available(product_id)
        if not product:
            raise ProductNotFound()

        cart_item = await self._get_cart_item(user_id, product_id)
        if not cart_item:
            raise CartNotFound()

        cart_item.quantity = quantity
        await self.cart_repo.add_cart_item(cart_item)

        return await self._get_cart_item(user_id, product_id)


    async def delete_item(self, user_id: int, product_id: int):
        product = await self._ensure_product_available(product_id)
        if not product:
            raise ProductNotFound()

        cart_item = await self._get_cart_item(user_id, product_id)
        if not cart_item:
            raise CartNotFound()

        await self.cart_repo.delete_cart_item(cart_item)



    async def clear_cart(self, user_id: int):
        await self.cart_repo.clear_cart(user_id)



