"""
Добавление параметров настроек из файла `./settings.py` в
переменные окружения, для использования этих параметров
в любой точке программы
"""

__all__ = ["mount_env", "AllowedNamesTypeFromSettings", "BaseSetting"]

from abc import abstractclassmethod
from os import environ
from typing import Optional, Any, Type

from vetcin_pack_fastapi.mount_logic import BaseMount


class AllowedNamesTypeFromSettings():
    """
    Список поддерживаемых переменных в файле с настройками

    None - подразумевает что эти переменные обязательны для переопределения

    Эти переменные будут доступны в переменных окружениях интерпретатора `os.environ`
    """
    """Пути"""
    #: Полный путь к Django приложению
    BASE_DIR: str = None
    #: Полный путь к проекту
    ROOT_DIR: str = None
    #: Путь к папке со статическими файлами
    #: FastApi будет маршрутизировать папку со статическими файлами,
    #: если вы хотите это делать с помощью Nginx то установите пустую строку ''
    STATIC_PATH: str = None
    """Админ панель"""
    #: Url подключения к БД ``СУБД+ДРАЙВЕР://USER:PASSWORD@HOST/ИМЯ_БД``
    SQLALCHEMY_DATABASE_URL: str = None
    #: Имя админа
    ADMIN_USER_NAME: str = ''
    #: Пароль от админ панели
    ADMIN_PASSWORD: str = ''
    """Отчетность"""
    #: Все добавленные приложения
    ALL_APP: str = ""
    #: Все добавленные модели
    ALL_MODEL: str = ""
    """Другое"""
    #: На коком хосту запустить веб сервер
    HOST_WEB: Optional[int] = "0.0.0.0"
    #: На коком порту запустить веб сервер
    PORT_WEB: Optional[int] = "8080"
    #: Авто перезагрузка сервера
    RELOAD_WEB: bool = True

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


class BaseSetting(AllowedNamesTypeFromSettings):
    """Шаблон для настроек"""

    class Mount(BaseMount):
        @abstractclassmethod
        def mount_app(self):
            ...


def mount_env(settings_obj: Type[BaseSetting]):
    """
    Подключаем переменные окружения
    """
    __read_params_from_settings_file(settings_obj)


def __read_params_from_settings_file(settings_obj: Type[BaseMount]):
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
