from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_zero.settings import Settings

engine = create_async_engine(
    Settings().DATABASE_URL,
    max_overflow=10,
    pool_size=5
)


# ##-> o "# pragma: no cover" serve para anular a necessidade de teste
async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
