import pytest
from starlette import status

from app.tests.conftest import create_auth_client


@pytest.mark.asyncio
async def test_get_all_categories(create_auth_client):
    client = await create_auth_client("a@test.com", "123456789", "admin")
    response = await client.get("/categories/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_and_create_category(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    response = await admin.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Electronics"

    category_id = response.json()["id"]

    response = await admin.get(f"/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Electronics"


@pytest.mark.asyncio
async def test_get_and_create_category_errors(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})
    response = await admin.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == status.HTTP_409_CONFLICT

    response = await admin.get(f"/categories/{999}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_category(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    response = await admin.put("/categories/1", json={"name": "Test_name"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test_name"


@pytest.mark.asyncio
async def test_update_category_errors(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    response = await admin.put("/categories/2", json={"name": "Test_name"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await admin.put("/categories/1", json={"name": "Test_name", "parent_id": 1})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_delete_category(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    response = await admin.delete("/categories/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_category_errors(create_auth_client):
    admin = await create_auth_client("a@gmail.com", "123456789", "admin")
    await admin.post("/categories/", json={"name": "Electronics"})

    response = await admin.delete("/categories/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

