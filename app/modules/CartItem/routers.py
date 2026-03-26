from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependcies import get_current_user
from app.core.dependcies import get_cart_service
from app.core.exceptions import NotFound
from app.modules.CartItem.schemas import CartItem as CartItemSchema, CartItemUpdate, Cart, CartItemCreate
from app.modules.CartItem.services import CartService
from app.modules.users.models import User



router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.get("/", response_model=Cart)
async def get_cart(
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
) -> Cart:

    cart = await cart_service.get_user_cart_items(current_user.id)
    return cart


@router.post("/items", response_model=CartItemSchema, status_code=status.HTTP_201_CREATED)
async def add_item(
    payload: CartItemCreate,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
) -> CartItemSchema:
    try:
        cart_item = await cart_service.add_item_to_cart(
        current_user.id,
        payload.product_id,
        payload.quantity,
        )
    except NotFound("Product not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return cart_item


@router.put("/items/{product_id}", response_model=CartItemSchema)
async def update_item(
    product_id: int,
    payload: CartItemUpdate,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    try:
        cart_item = await cart_service.update_item(payload.quantiny, product_id, current_user.id)
    except NotFound("Product not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except NotFound("Cart not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return cart_item

@router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    product_id: int,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    try:
        await cart_service.delete_item(product_id, current_user.id)
    except NotFound("Product not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except NotFound("Cart not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")




@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    await cart_service.clear_cart(current_user.id)
    await cart_service.commit()