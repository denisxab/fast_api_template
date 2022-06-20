"""
Добавление параметров настроек из файла `./settings.py` в
переменные окружения, для использования этих параметров
в любой точке программы
"""

__all__ = ["mount_env", "AllowedNamesTypeFromSettings", "BaseSettings"]

import re
from abc import abstractclassmethod
from os import environ
from pathlib import Path
from typing import Optional, Any, Type

from vetcin_pack_fastapi.mount_logic import BaseMount


class AllowedNamesTypeFromSettings():
    """
    Список поддерживаемых переменных в файле с настройками

    None - подразумевает что эти переменные обязательны для переопределения

    Эти переменные будут доступны в переменных окружениях интерпретатора `os.environ`
    """
    """Пути"""
    #: Полный путь к проекту FASTAPI
    BASE_DIR: Path = None
    #: Полный путь к проекту (на 1 уровень выше)
    ROOT_DIR: Path = None
    #: Путь к папке со статическими файлами
    #: FastApi будет маршрутизировать папку со статическими файлами,
    #: если вы хотите это делать с помощью Nginx то установите пустую строку ''
    STATIC_PATH: Path = None
    """БД"""
    #: Url подключения к БД ``СУБД+ДРАЙВЕР://USER:PASSWORD@HOST:PORT/ИМЯ_БД``
    SQLALCHEMY_DATABASE_URL: str = None
    """Сервер"""
    #: На коком хосту запустить веб сервер
    HOST_WEB: Optional[str] = "0.0.0.0"
    #: На коком порту запустить веб сервер
    PORT_WEB: Optional[int] = "8080"
    #: Авто перезагрузка сервера
    RELOAD_WEB: bool = True
    """Отчетность"""
    #: Все добавленные приложения
    ALL_APP: str = ""
    #: Все добавленные SQL модели
    ALL_MODEL: str = ""
    """Админ панель"""
    #: Имя админа
    ADMIN_USER_NAME: str = ''
    #: Пароль от админ панели
    ADMIN_PASSWORD: str = ''

    @classmethod
    def default_dit(cls, **kwargs):
        """Вернуть словарь в виде `атрибут:значение`"""
        return {_k: _v for _k, _v
                in cls.__dict__.items() if
                not _k.startswith("__") and
                not _k.endswith("__") and
                _k not in kwargs} | kwargs


#: Доступные настройки
AllowedNames: dict[str, Any] = AllowedNamesTypeFromSettings.default_dit()


class BaseSettings(AllowedNamesTypeFromSettings):
    """Шаблон для настроек"""

    class Mount(BaseMount):
        @abstractclassmethod
        def mount_app(self):
            ...


def mount_env(settings_obj: Type[BaseSettings]):
    """
    Подключаем переменные окружения
    """
    __read_params_from_settings_file(settings_obj)


def __read_params_from_settings_file(settings_obj: Type[BaseSettings]):
    """
    Прочитать файл с настройками и занести их
    в переменные окружения интерпретатора
    """
    implemented = set()
    # Получить переменные из файла конфигурации.
    for _k, _v in settings_obj.__dict__.items():
        # Если имя конфигурации разрешено, то добавляем его в переменные окружения
        if _k in AllowedNames:
            environ[_k] = str(_v)
            implemented.add(_k)
    # Для не переопределенных переменных берем значения по умолчанию
    for _no_implemented in set(AllowedNames.keys()) - implemented:
        # Если переменная обязательна для переопределения, то вызываем исключение
        if AllowedNames[_no_implemented] is None:
            raise KeyError(f"В файле настроек `settings.py` не реализована переменная {_no_implemented}")
        else:
            environ[_no_implemented] = str(AllowedNames[_no_implemented])


def read_env_file(file_name: str) -> dict[str, str]:
    """Чтение переменных окружения из указанного файла, и добавление их в ПО `python`"""
    with open(file_name, 'r', encoding='utf-8') as _file:
        res = {}
        for line in _file:
            tmp = re.sub(r'^#[\s\w\d\W\t]*|[\t\s]', '', line)
            if tmp:
                k, v = tmp.split('=', 1)
                # Если значение заключено в двойные кавычки, то нужно эти кавычки убрать
                if v.startswith('"') and v.endswith('"'):
                    v = v[1:-1]
                res[k] = v
    return res
