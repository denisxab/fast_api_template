"""
Файл с настройками проекта
"""
__all__ = ["mount_env", "AllowedNames"]

from os import environ

from fast_xabhelper.helpful import read_file_by_module

# Список поддерживаемых переменных в файле с настройками
AllowedNames: set[str] = {
    "SQLALCHEMY_DATABASE_URL",
    "BASE_DIR",
    "ROOT_DIR",
    "COPY_STATIC",
    "ADMIN_USER_NAME",
    "ADMIN_PASSWORD",
    "ALL_APP"
}


def mount_env(_path: str = "./settings.py"):
    """
    Подключаем переменные окружения
    """
    __read_settings_file(_path)


def __read_settings_file(_path: str):
    """
    Прочитать файл с настройками
    """
    __module = read_file_by_module(_path)
    # Получить переменные из файла конфигурации.
    for _k, _v in __module.__dict__.items():
        # Если имя конфигурации разреженно, то добавляем его в переменные окружения
        if _k in AllowedNames:
            environ[_k] = str(_v)
