import pytest
from starlette import status


@pytest.mark.asyncio
async def test_get_cart(test_client):
    response = await test_client.get("/cart/")
    assert response.status_code == status.HTTP_200_OK
