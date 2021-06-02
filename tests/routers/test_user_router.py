import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_user_endpoint(authenticated_api_client, faker):
    response = await authenticated_api_client.post(
        "/users/", json={"username": faker.user_name(), "password": faker.password()}
    )
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert tuple(response.json().keys()) == ("access_token", "token_type")


@pytest.mark.asyncio
async def test_create_user_endpoint_user_already_exists(
    authenticated_api_client, user, faker
):
    response = await authenticated_api_client.post(
        "/users/", json={"username": user.username, "password": faker.password()}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()


@pytest.mark.asyncio
async def test_profile_me_endpoint(authenticated_api_client):
    response = await authenticated_api_client.get("/users/me")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_invalid_current_user(api_client):
    response = await api_client.get(
        "/users/me", headers={"Authorization": "Bearer xpto"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
