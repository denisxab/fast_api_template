"""
Файл с настройками проекта
"""
__all__ = ["mount_env", "AllowedNamesType"]

from os import environ
from typing import TypedDict, Optional, Any

from mg_file.file.base_file import read_file_by_module


class AllowedNamesType(TypedDict):
    """
    Список поддерживаемых переменных в файле с настройками
    """

    """
    Пути
    """
    # Полный путь к Django приложению
    BASE_DIR: Optional[str]
    # Полный путь к проекту
    ROOT_DIR: Optional[str]
    # Путь к папке со статическими файлами
    STATIC_PATH: Optional[str]
    """
    Админ панель
    """
    # Url подключения к БД "postgresql+asyncpg://postgres:root@localhost/fast"
    SQLALCHEMY_DATABASE_URL: Optional[str]
    # Имя админа
    ADMIN_USER_NAME: Optional[str]
    # Пароль от админ панели
    ADMIN_PASSWORD: Optional[str]
    """
    Отчетность
    """
    # Все добавленные приложения
    ALL_APP: str
    # Все добавленные модели
    ALL_MODEL: str
    """
    Другое
    """
    # Нудно ли копировать статические файлы
    COPY_STATIC: bool


AllowedNames: dict[str, Any] = AllowedNamesType(
    BASE_DIR=None,
    ROOT_DIR=None,
    SQLALCHEMY_DATABASE_URL=None,
    ADMIN_USER_NAME=None,
    ADMIN_PASSWORD=None,
    ALL_APP="",
    ALL_MODEL="",
    STATIC_PATH=None,
    COPY_STATIC=True,
)


def mount_env(_path: str = "./settings.py"):
    """
    Подключаем переменные окружения
    """
    __read_settings_file(_path)


def __read_settings_file(_path: str):
    """
    Прочитать файл с настройками
    """

    implemented = set()

    __module = read_file_by_module(_path)
    # Получить переменные из файла конфигурации.
    for _k, _v in __module.__dict__.items():
        # Если имя конфигурации разреженно, то добавляем его в переменные окружения
        if _k in AllowedNames:
            environ[_k] = str(_v)
            implemented.add(_k)

    # Для не переопределенных переменных берем значения по умолчанию
    for _no_implemented in set(AllowedNames.keys()) - implemented:
        # Если переменная обязательна для переопределения, то вызываем исключение
        if AllowedNames[_no_implemented] is None:
            raise KeyError(f"Не реализована переменная {_no_implemented}")
        environ[_no_implemented] = str(AllowedNames[_no_implemented])
