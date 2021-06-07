import pytest
from fastapi import status
from mixer.backend.sqlalchemy import mixer
from sqlalchemy import update

from poc_fastapi.models import Post


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


@pytest.mark.asyncio
async def test_delete_post_endpoint(authenticated_api_client, post):
    response = await authenticated_api_client.delete(f"/posts/{post.uuid}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()


@pytest.mark.asyncio
async def test_delete_post_endpoint_from_another_user(
    authenticated_api_client, post, session
):
    user = mixer.blend("poc_fastapi.models.user.User")
    session.add(user)
    await session.commit()

    await session.execute(
        update(Post, values={Post.owner_id: user.id}).where(Post.id == post.id)
    )
    await session.commit()
    response = await authenticated_api_client.delete(f"/posts/{post.uuid}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()
