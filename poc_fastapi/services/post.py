from sqlalchemy.ext.asyncio import AsyncSession

from poc_fastapi.models.post import Post
from poc_fastapi.schemas.post import PostInSchema


async def create_post(
    session: AsyncSession, post_schema: PostInSchema, owner_id: int
) -> Post:
    post = Post(content=post_schema.content, owner_id=owner_id)
    session.add(post)
    return post
