from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from poc_fastapi.db.base import get_session
from poc_fastapi.exceptions import InvalidCredentials, UserNotFound
from poc_fastapi.models.user import User
from poc_fastapi.schemas.user import UserInSchema

http_bearer = HTTPBearer()


async def create_user(session: AsyncSession, user_schema: UserInSchema) -> User:
    user = User(username=user_schema.username)
    user.set_password(user_schema.password)
    session.add(user)
    return user


async def get_user_by_uuid(session: AsyncSession, user_uuid: UUID) -> User:
    result = await session.execute(select(User).where(User.uuid == user_uuid))
    first_result = result.first()
    if not first_result:
        raise UserNotFound
    return first_result[0]


async def create_access_token(
    user: User, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
):
    data = {
        "sub": str(user.uuid),
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes),
    }
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    http_credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(
            http_credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_uuid: UUID = UUID(payload["sub"])
        user = await get_user_by_uuid(session, user_uuid)
    except Exception as e:
        raise InvalidCredentials from e
    return user
