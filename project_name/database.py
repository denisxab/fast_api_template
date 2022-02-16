from hashlib import sha512
from random import randint

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/fast"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# Получить сессию
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# Получить сессию в транзакции
async def get_session_transaction() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session


# Захешировать пароль
def hashPassword(password: str) -> str:
    return sha512(password.encode('utf-8')).hexdigest()


# Случайный хеш
def hashRandom() -> str:
    return hashPassword(str(randint(0, 1000)))
