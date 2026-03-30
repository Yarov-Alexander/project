import pytest

@pytest.mark.asyncio
async def test_create_user(create_auth_client):
    admin = await create_auth_client("b@test.com", "123456789", "admin")