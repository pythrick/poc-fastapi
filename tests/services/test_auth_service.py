from uuid import UUID

import pytest
from jose import jwt

from config import ALGORITHM, SECRET_KEY
from poc_fastapi.exceptions import AuthenticationError
from poc_fastapi.services.auth import authenticate


@pytest.mark.asyncio
async def test_authenticate(session, user, faker):
    password = faker.password()
    user.set_password(password)
    session.add(user)
    await session.commit()
    access_token = await authenticate(session, user.username, password)
    payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    user_uuid = UUID(payload["sub"])
    assert user_uuid == user.uuid


@pytest.mark.asyncio
async def test_authenticate_invalid_credentials(session, user, faker):
    password = faker.password()
    with pytest.raises(AuthenticationError):
        await authenticate(session, user.username, password)
