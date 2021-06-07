from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from poc_fastapi.exceptions import PostNotFoundError
from poc_fastapi.models.post import Post
from poc_fastapi.models.user import User
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


async def get_post_by_uuid(
    session: AsyncSession, post_uuid: UUID, owner: Optional[User] = None
) -> Post:
    query = select(Post).where(Post.uuid == post_uuid)
    if owner:
        query = query.where(Post.owner == owner)
    result = await session.execute(query)
    first_result = result.first()
    if not first_result:
        raise PostNotFoundError
    return first_result[0]


async def delete_post(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()
