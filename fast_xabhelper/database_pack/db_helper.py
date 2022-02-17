from hashlib import sha512
from random import randint
from typing import Any, TypedDict
from typing import Union

from sqlalchemy.orm.decl_api import DeclarativeMeta

from fast_xabhelper.froms import convert_sql_type_to_html_input_type


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
