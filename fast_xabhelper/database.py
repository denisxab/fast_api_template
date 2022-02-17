from hashlib import sha512
from os import environ
from random import randint
from typing import Any, Union

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy.sql.type_api import TypeEngine

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


def row2dict(row: DeclarativeMeta, list_display: list) -> tuple[dict[Any, dict[str, Any]], Union[list[Any], Any]]:
    """
    Получить имена атрибутов в модели БД
    """
    d = {}
    title = []
    for column in row.__table__.columns:
        if column.name in list_display:
            title.append(column.name)
            d[column.name] = {
                # Тип
                "type": column.type,
                # Тип для html формы
                "html_input_type": get_html_type(column.type),
                # Описание
                "description": column.description,
                # Внешние связи
                "foreign_keys": column.foreign_keys,
                # Разрешить Null
                "nullable": column.nullable,
                # Первичный ключ
                "primary_key": column.primary_key,
                # Уникальность
                "unique": column.unique,
            }
    return d, title


CONVERT_SQL_TYPE_TO_HTML_INPUT_TYPE: dict[str, str] = {
    'INTEGER': "number",
    "VARCHAR": "text",
    "BOOLEAN": "radio"
}


def get_html_type(sql_type: TypeEngine):
    return CONVERT_SQL_TYPE_TO_HTML_INPUT_TYPE.get(str(sql_type), None)


# Захешировать пароль
def hashPassword(password: str) -> str:
    return sha512(password.encode('utf-8')).hexdigest()


# Случайный хеш
def hashRandom() -> str:
    return hashPassword(str(randint(0, 1000)))
