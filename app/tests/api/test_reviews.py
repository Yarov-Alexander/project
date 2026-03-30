import pytest


@pytest.mark.asyncio
async def test_post_reviews(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    buyer = await create_auth_client("buyer@test.com", "123456789", "buyer")
    response = await buyer.post("/reviews/", json={"product_id": 1, "grade": 5, "comment": "Nice Good"})
    assert response.status_code == 201
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["grade"] == 5
    assert response.json()[0]["comment"] == "Nice Good"


@pytest.mark.asyncio
async def test_post_reviews_errors(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    buyer = await create_auth_client("buyer@test.com", "123456789", "buyer")
    response = await seller.post("/reviews/", json={"product_id": 1, "grade": 5, "comment": "Nice Good"})
    assert response.status_code == 403
    response = await buyer.post("/reviews/", json={"product_id": 1, "grade": 6, "comment": "Nice Good"})
    assert response.status_code == 422
    response = await buyer.post("/reviews/", json={"product_id": 999, "grade": 5, "comment": "Nice Good"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_reviews_by_id(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    buyer = await create_auth_client("buyer@test.com", "123456789", "buyer")
    await buyer.post("/reviews/", json={"product_id": 1, "grade": 5, "comment": "Nice Good"})

    response = await seller.get("/reviews/products/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_reviews_by_id(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    buyer = await create_auth_client("buyer@test.com", "123456789", "buyer")
    await buyer.post("/reviews/", json={"product_id": 1, "grade": 5, "comment": "Nice Good"})
    response = await buyer.post("/reviews/", json={"product_id": 2, "grade": 5, "comment": "Nice Good"})
    assert response.status_code == 404
    response = await seller.get("/reviews/products/2")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_by_id(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    buyer = await create_auth_client("buyer@test.com", "123456789", "buyer")
    await buyer.post("/reviews/", json={"product_id": 1, "grade": 5, "comment": "Nice Good"})

    response = await seller.delete("/reviews/1")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_by_id_error(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")
    # Создаем категорию и продукт
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    buyer = await create_auth_client("buyer@test.com", "123456789", "buyer")
    await buyer.post("/reviews/", json={"product_id": 1, "grade": 5, "comment": "Nice Good"})

    response = await seller.delete("/reviews/2")
    assert response.status_code == 404