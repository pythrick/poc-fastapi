from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from poc_fastapi.db.base import get_session
from poc_fastapi.models import User
from poc_fastapi.schemas.post import PostInSchema, PostSchema
from poc_fastapi.services import post as post_service
from poc_fastapi.services.user import get_current_active_user
from poc_fastapi.validators.permission import PermissionValidator

router = APIRouter(prefix="/posts", tags=["posts"])

has_create_post_permission = PermissionValidator(
    required_perms={"create-post"}, allowed_roles={"writer"}
)


@router.get("/", response_model=List[PostSchema])
async def list_posts_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[PostSchema]:
    ...


@router.post(
    "/",
    response_model=PostSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(has_create_post_permission)],
)
async def create_post_endpoint(
    post: PostInSchema,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
) -> PostSchema:
    post_db = await post_service.create_post(session, post, current_user.id)
    await session.commit()
    return PostSchema.from_orm(post_db)
