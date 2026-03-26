from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

from app.modules.products.schemas import Product


class CartItemCreate(BaseModel):

    product_id: int = Field(description="ID товара")
    quantity: int = Field(ge=1, description="Количество товара")
    model_config = ConfigDict(from_attributes=True)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1, description="Количество товара")


class CartItem(BaseModel):
    id: int = Field(..., description="ID позиции корзины")
    quantity: int = Field(..., ge=1, description="Количество товара")
    product: Product = Field(description="ID товара")

    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    items: list["CartItem"] = Field(default_factory=list, description="Содержимое корзины")
    total_quantity: int = Field(..., ge=0, description="Общее количество товаров")
    total_price: Decimal = Field(..., ge=0, description="Общая стоимость товаров")

    model_config = ConfigDict(from_attributes=True)