from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependcies import get_current_user
from app.core.dependcies import get_cart_service
from app.modules.CartItem.schemas import CartItem as CartItemSchema, CartItemUpdate, Cart, CartItemCreate
from app.modules.CartItem.services import CartService
from app.modules.users.models import User
from decimal import Decimal


router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.get("/", response_model=Cart)
async def get_cart(
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    items = await cart_service.get_user_cart_items(current_user.id)

    total_quantity = sum(item.quantity for item in items)

    total_price = sum(
        Decimal(item.quantity) *
        (item.product.price if item.product.price else Decimal("0"))
        for item in items
    )

    return Cart(
        user_id=current_user.id,
        items=items,
        total_quantity=total_quantity,
        total_price=total_price
    )

@router.post("/items", response_model=CartItemSchema, status_code=201)
async def add_item(
    payload: CartItemCreate,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    product = await cart_service._ensure_product_available(payload.product_id)

    if not product:
        raise HTTPException(404, "Product not found")

    cart_item = await cart_service._get_cart_item(
        current_user.id,
        payload.product_id
    )

    if cart_item:
        cart_item.quantity += payload.quantity
    else:
        cart_item = await cart_service.create_item(
            current_user.id,
            payload.product_id,
            payload.quantity
        )

    await cart_service.commit()

    return await cart_service._get_cart_item(
        current_user.id,
        payload.product_id
    )

@router.put("/items/{product_id}", response_model=CartItemSchema)
async def update_item(
    product_id: int,
    payload: CartItemUpdate,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    product = await cart_service._ensure_product_available(product_id)

    if not product:
        raise HTTPException(404, "Product not found")

    cart_item = await cart_service._get_cart_item(
        current_user.id,
        product_id
    )

    if not cart_item:
        raise HTTPException(404, "Cart item not found")

    cart_item.quantity = payload.quantity
    await cart_service.commit()

    return await cart_service._get_cart_item(
        current_user.id,
        product_id
    )


@router.delete("/items/{product_id}", status_code=204)
async def delete_item(
    product_id: int,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    cart_item = await cart_service._get_cart_item(
        current_user.id,
        product_id
    )

    if not cart_item:
        raise HTTPException(404, "Cart item not found")

    await cart_service.delete_item(cart_item)
    await cart_service.commit()


@router.delete("/", status_code=204)
async def clear_cart(
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    await cart_service.clear_cart(current_user.id)
    await cart_service.commit()