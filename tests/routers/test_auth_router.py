import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_access_token_endpoint(api_client, session, user, faker):
    password = faker.password()
    user.set_password(password)
    session.add(user)
    await session.commit()
    response = await api_client.post(
        "/auth/token", json={"username": user.username, "password": password}
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert tuple(response.json().keys()) == ("access_token", "token_type")
