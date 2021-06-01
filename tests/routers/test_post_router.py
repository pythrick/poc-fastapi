import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_post_endpoint(authenticated_api_client):
    response = await authenticated_api_client.post("/posts/", json={"content": "xpto"})
    assert response.status_code == status.HTTP_201_CREATED, response.json()
