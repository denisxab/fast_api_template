from hashlib import sha512
from os import environ
from random import randint
from typing import Any, Union, TypedDict

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from fast_xabhelper.froms import convert_sql_type_to_html_input_type

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


class ExtendColumn(TypedDict):
    # Тип
    type: Any
    # Тип для html формы
    html_input_type: str
    # Описание
    description: str
    # Внешние связи
    foreign_keys: Any
    # Разрешить Null
    nullable: bool
    # Первичный ключ
    primary_key: Any
    # Уникальность
    unique: bool


def row2dict(row: DeclarativeMeta, list_display: list) -> tuple[dict[Any, dict[str, Any]], Union[list[Any], Any]]:
    """
    Получить имена атрибутов в модели БД
    """
    extend_column: dict[str, Any] = {}
    title_column: list[str] = []
    for column in row.__table__.columns:
        if column.name in list_display:
            title_column.append(column.name)
            extend_column[column.name] = ExtendColumn(
                type=column.type,
                html_input_type=convert_sql_type_to_html_input_type(column.type),
                description=column.description,
                foreign_keys=column.foreign_keys,
                nullable=column.nullable,
                primary_key=column.primary_key,
                unique=column.unique,
            )
    return extend_column, title_column


# Захешировать пароль
def hashPassword(password: str) -> str:
    return sha512(password.encode('utf-8')).hexdigest()


# Случайный хеш
def hashRandom() -> str:
    return hashPassword(str(randint(0, 1000)))
