from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from poc_fastapi.models.post import Post
from poc_fastapi.schemas.post import PostInSchema


async def create_post(
    session: AsyncSession, post_schema: PostInSchema, owner_id: int
) -> Post:
    post = Post(content=post_schema.content, owner_id=owner_id)
    session.add(post)
    return post


async def list_posts(
    session: AsyncSession, limit: int = 10, offset: int = 1
) -> List[Post]:
    result = await session.execute(select(Post).offset(offset).limit(limit))
    return [post for post, in result.all()]
