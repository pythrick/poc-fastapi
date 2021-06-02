from uuid import uuid4

import pytest

from poc_fastapi.exceptions import UserNotFound
from poc_fastapi.models import User
from poc_fastapi.services.user import get_user_by_username, get_user_by_uuid


@pytest.mark.asyncio
async def test_get_user_by_uuid(session, user):
    user = await get_user_by_uuid(session, user.uuid)
    assert isinstance(user, User)


@pytest.mark.asyncio
async def test_get_user_by_uuid_not_found(session):
    with pytest.raises(UserNotFound):
        await get_user_by_uuid(session, uuid4())


@pytest.mark.asyncio
async def test_get_user_by_username(session, user):
    user = await get_user_by_username(session, user.username)
    assert isinstance(user, User)


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(session, faker):
    with pytest.raises(UserNotFound):
        await get_user_by_username(session, faker.pystr())
