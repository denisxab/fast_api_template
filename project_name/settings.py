"""
Файл с настройками проекта
"""
from os import environ
from pathlib import Path


def mount_env():
    """
    Подключаем переменные окружения
    """
    """
    БД
    """
    # Url подключения к БД "postgresql+asyncpg://postgres:root@localhost/fast"
    environ["SQLALCHEMY_DATABASE_URL"] = "postgresql+asyncpg://postgres:root@localhost/fast"
    """
    Пути
    """
    # Полный путь к Django приложению
    BASE_DIR = Path(__file__).resolve().parent
    environ["BASE_DIR"] = str(BASE_DIR)
    # Полный путь к проекту
    environ["ROOT_DIR"] = "/".join(str(BASE_DIR).split('/')[:-1])
    """
    Статические файлы
    """
    # Нудно ли копировать статические файлы
    environ["COPY_STATIC"] = "False"
    """
    Админ панель
    """
    # Имя админа
    environ["ADMIN_USER_NAME"] = "denis"
    # Пароль от админ панели
    environ["ADMIN_PASSWORD"] = "321"
    """
    Все добавленные приложения
    """
    environ["ALL_APP"] = ""
