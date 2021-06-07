from typing import Set
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from config import ALGORITHM, HTTP_BEARER, SECRET_KEY
from poc_fastapi.db.base import get_session
from poc_fastapi.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from poc_fastapi.models.user import User
from poc_fastapi.schemas.user import UserInSchema


async def create_user(session: AsyncSession, user_schema: UserInSchema) -> User:
    user = User(username=user_schema.username)
    user.set_password(user_schema.password)
    session.add(user)
    return user


async def get_user_by_uuid(session: AsyncSession, user_uuid: UUID) -> User:
    result = await session.execute(select(User).where(User.uuid == user_uuid))
    first_result = result.first()
    if not first_result:
        raise UserNotFoundError
    return first_result[0]


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    result = await session.execute(select(User).where(User.username == username))
    first_result = result.first()
    if not first_result:
        raise UserNotFoundError
    return first_result[0]


async def get_current_active_user(
    http_credentials: HTTPAuthorizationCredentials = Depends(HTTP_BEARER),
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(
            http_credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_uuid: UUID = UUID(payload["sub"])
        user = await get_user_by_uuid(session, user_uuid)
        if not user.is_active:
            raise InactiveUserError
    except Exception as e:
        raise InvalidCredentialsError from e
    return user


async def list_user_perms(user: User) -> Set[str]:
    # TODO: Create real implementation
    return {"create-post", "edit-post", "read-post", "delete-post", "list-post"}


async def list_user_roles(user: User) -> Set[str]:
    # TODO: Create real implementation
    return {
        "reader",
        "writer",
        "reviewer",
        "publisher",
        "maintainer",
    }  # admin
