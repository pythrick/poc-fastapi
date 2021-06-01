import pytest
from httpx import AsyncClient
from mixer.backend.sqlalchemy import mixer

from poc_fastapi.app import app
from poc_fastapi.db.base import async_session, init_models
from poc_fastapi.services.user import create_access_token


@pytest.fixture(autouse=True)
async def db():
    await init_models()


@pytest.fixture()
async def session():
    async with async_session() as session:
        yield session


@pytest.fixture()
async def api_client():
    async with AsyncClient(app=app, base_url="http://testing") as client:
        yield client


@pytest.fixture()
def token(user, event_loop):
    return event_loop.run_until_complete(create_access_token(user))


@pytest.fixture()
async def authenticated_api_client(user, token):
    async with AsyncClient(
        app=app, base_url="http://testing", headers={"Authorization": f"Bearer {token}"}
    ) as client:
        yield client


@pytest.fixture()
def user(session, event_loop):
    obj = mixer.blend("poc_fastapi.models.user.User")
    session.add(obj)
    event_loop.run_until_complete(session.commit())
    return obj


@pytest.fixture()
def post(session, user, event_loop):
    obj = mixer.blend("poc_fastapi.models.post.Post", owner=user)
    session.add(obj)
    event_loop.run_until_complete(session.commit())
    return obj
