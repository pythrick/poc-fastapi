from sqlalchemy.ext.asyncio import AsyncSession


async def health_check(session: AsyncSession) -> None:
    await session.execute("SELECT 1")
