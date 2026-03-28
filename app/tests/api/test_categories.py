import pytest
from starlette import status


@pytest.mark.asyncio
async def test_get_all_categories(test_client):
    response = await test_client.get("/categories/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_and_create_category(auth_client):
    # создаём категорию
    response = await auth_client.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Electronics"

    category_id = response.json()["id"]

    # получаем категорию
    response = await auth_client.get(f"/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Electronics"