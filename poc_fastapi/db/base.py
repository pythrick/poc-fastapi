from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

async_engine = create_async_engine(config.DATABASE_URL)

Base = declarative_base()

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    if config.FASTAPI_ENV == "testing":
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
