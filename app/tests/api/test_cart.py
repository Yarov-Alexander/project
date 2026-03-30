
import pytest
from starlette import status

from app.tests.conftest import create_auth_client


@pytest.mark.asyncio
async def test_get_cart(create_auth_client):
    buyer = await create_auth_client("b@test.com", "123456789", "buyer")
    response = await buyer.get("/cart/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_add_item_to_cart(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    response_category = await admin.post("/categories/", json={"name": "Electronics"})
    assert response_category.status_code == status.HTTP_201_CREATED

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    response_product = await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    assert response_product.status_code == status.HTTP_201_CREATED

    response_cart_item = await admin.post("/cart/items", json={"product_id": 1, "quantity": 1})
    assert response_cart_item.status_code == status.HTTP_201_CREATED
    assert response_cart_item.json()["quantity"] == 1
    assert response_cart_item.json()["products"]["id"] == 1


@pytest.mark.asyncio
async def test_add_nonexistent_product_to_cart(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")

    # Попытка добавить товар, которого нет
    response = await admin.post("/cart/items", json={"product_id": 999, "quantity": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@pytest.mark.asyncio
async def test_add_item_with_invalid_quantity(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")

    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})
    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    # Передача невалидного количества (0)
    response = await admin.post("/cart/items", json={"product_id": 1, "quantity": 0})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_put_cart_item(create_auth_client):
    seller = await create_auth_client("s@test.com", "123456789", "seller")
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    await admin.post("/cart/items", json={"product_id": 1, "quantity": 1})

    response_cart = await admin.put("/cart/items/1", json={"quantity": 2})
    assert response_cart.status_code == status.HTTP_200_OK
    response_cart = await admin.get("/cart/")
    assert response_cart.json()["total_quantity"] == 2



@pytest.mark.asyncio
async def test_put_cart_item_errors(create_auth_client):
    seller = await create_auth_client("s@test.com", "123456789", "seller")
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    await admin.post("/cart/items", json={"product_id": 1, "quantity": 1})

    response_cart = await admin.put("/cart/items/2", json={"quantity": 2})
    assert response_cart.status_code == status.HTTP_404_NOT_FOUND
    response_cart = await admin.put("/cart/items/1", json={"quantity": -1})
    assert response_cart.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT





@pytest.mark.asyncio
async def test_delete_cart_by_id(create_auth_client):
    seller = await create_auth_client("s@test.com", "123456789", "seller")
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    await admin.post("/cart/items", json={"product_id": 1, "quantity": 1})

    response_cart = await admin.delete("/cart/items/1")
    assert response_cart.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_cart_by_id_error(create_auth_client):
    seller = await create_auth_client("s@test.com", "123456789", "seller")
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    await admin.post("/cart/items", json={"product_id": 1, "quantity": 1})

    response_cart = await admin.delete("/cart/items/2")
    assert response_cart.status_code == status.HTTP_404_NOT_FOUND