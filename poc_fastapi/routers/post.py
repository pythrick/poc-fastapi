from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from poc_fastapi.db.base import get_session
from poc_fastapi.models import User
from poc_fastapi.schemas.params import ParamsSchema
from poc_fastapi.schemas.post import PostInSchema, PostSchema
from poc_fastapi.services import post as post_service
from poc_fastapi.services.user import get_current_active_user
from poc_fastapi.validators.permission import PermissionValidator

router = APIRouter(prefix="/posts", tags=["posts"])

has_create_post_permission = PermissionValidator(
    required_perms={"create-post"}, allowed_roles={"writer"}
)
has_list_post_permission = PermissionValidator(
    required_perms={"list-post"}, allowed_roles={"reader"}
)
has_delete_post_permission = PermissionValidator(
    required_perms={"delete-post"}, allowed_roles={"maintainer"}
)


@router.get(
    "/",
    response_model=List[PostSchema],
    dependencies=[Depends(has_list_post_permission)],
)
async def list_posts_endpoint(
    params: ParamsSchema = Depends(),
    session: AsyncSession = Depends(get_session),
) -> List[PostSchema]:
    posts = await post_service.list_posts(
        session, limit=params.limit, offset=params.skip
    )
    return [PostSchema.from_orm(p) for p in posts]


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


@router.delete(
    "/{post_id}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(has_delete_post_permission)],
)
async def delete_post_endpoint(
    post_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    post = await post_service.get_post_by_uuid(session, post_id, owner=current_user)
    await post_service.delete_post(session, post)
