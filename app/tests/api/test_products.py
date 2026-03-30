import pytest

@pytest.mark.asyncio
async def test_post_products(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    response = await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    assert response.status_code == 201
    assert response.json().get("name") == "Iphone 18 Pro Max"
    assert response.json().get("price") == "1000.00"


@pytest.mark.asyncio
async def test_post_products_error(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    response = await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 2})
    assert response.status_code == 404
    response = await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": -1, "stock": 50, "category_id": 1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_products_by_id(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/",json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    response = await seller.get("/products/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_products_by_id_error(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/",json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    response = await seller.get("/products/2")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_product(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    response = await seller.put("/products/1", json={"name": "Iphone 20 Pro Max", "price": 2000, "stock": 50, "category_id": 1})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_product_error(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    response = await seller.put("/products/999", json={"name": "Iphone 20 Pro Max", "price": 2000, "stock": 50, "category_id": 1})
    assert response.status_code == 404
    seller = await create_auth_client("a@test.com", "123456789", "seller")
    response = await seller.put("/products/1", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_product(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    response = await seller.delete("/products/1")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_product_errors(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    seller = await create_auth_client("s@test.com", "123456789", "seller")
    await seller.post("/products/", json={"name": "Iphone 18 Pro Max", "price": 1000, "stock": 50, "category_id": 1})

    response = await seller.delete("/products/2")
    assert response.status_code == 404
    seller = await create_auth_client("h@test.com", "123456789", "seller")
    response = await seller.delete("/products/1")
    assert response.status_code == 403


