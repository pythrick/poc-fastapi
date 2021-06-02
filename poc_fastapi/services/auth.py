from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from poc_fastapi.exceptions import AuthenticationError
from poc_fastapi.models import User
from poc_fastapi.services.user import get_user_by_username


async def create_access_token(
    user: User, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
):
    data = {
        "sub": str(user.uuid),
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes),
    }
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate(session: AsyncSession, username: str, password: str):
    try:
        user = await get_user_by_username(session, username)
        user.verify_password(password)
    except Exception as e:
        raise AuthenticationError from e
    return await create_access_token(user)
