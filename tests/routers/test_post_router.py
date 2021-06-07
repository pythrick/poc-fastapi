import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_post_endpoint(authenticated_api_client):
    response = await authenticated_api_client.post("/posts/", json={"content": "xpto"})
    assert response.status_code == status.HTTP_201_CREATED, response.json()


@pytest.mark.asyncio
async def test_list_posts_endpoint(authenticated_api_client, post):
    response = await authenticated_api_client.get("/posts/")
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json() == [
        {
            "uuid": str(post.uuid),
            "content": post.content,
            "owner": {"uuid": str(post.owner.uuid), "username": post.owner.username},
            "created_at": post.created_at.isoformat(),
        }
    ]
