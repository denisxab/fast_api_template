from os import environ

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    # "postgresql+asyncpg://postgres:root@localhost/fast"
    environ.get("SQLALCHEMY_DATABASE_URL", "")
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# Получить сессию
async def get_session() -> AsyncSession:
    # Получить сессию await get_session().__anext__()
    async with async_session() as session:
        yield session


# Получить сессию в транзакции
async def get_session_transaction() -> AsyncSession:
    # Получить сессию await get_session_transaction().__anext__()
    async with async_session() as session:
        async with session.begin():
            yield session


def get_session_dec(fun):
    async def wrapper(*arg, **kwargs):
        async with async_session() as session:
            res = await fun(*arg, **kwargs, session=session, )
        return res

    return wrapper
