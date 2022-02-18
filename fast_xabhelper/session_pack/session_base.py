"""
Файл для работы с сессиями
"""
from abc import abstractclassmethod
from datetime import datetime
from typing import Any, Optional, Callable

from mg_file import JsonFile

from fast_xabhelper.database_pack.db_helper import hashRandom

SESSION_NAME = "session_id"


class SESSION:
    data: dict[str, Any] = {}

    @classmethod
    def _get_hash(cls) -> str:
        return hashRandom()

    @abstractclassmethod
    def _run_callback_if_exists_hash(cls, response, hash_, callback: Callable):
        """Поучить данные по ключу"""
        ...

    @abstractclassmethod
    def crate_session(cls, response) -> str:
        """Создать сессию"""
        ...

    @abstractclassmethod
    def delete_session(cls, response, request) -> Optional[str]:
        """Удалить сессию"""
        ...

    @abstractclassmethod
    def _add(cls, hash_: str, key: str, value: Any):
        """Добавить данные в сессию"""
        ...

    @abstractclassmethod
    def get(cls, request, response, key: str) -> Any:
        """Получить данные из сессии"""
        ...

    @abstractclassmethod
    def keys(cls, request, response):
        """Получить ключи из сессии"""
        ...

    @abstractclassmethod
    def items(cls, request, response):
        """Получить все данные из сессии"""
        ...


class SESSION_RAM(SESSION):

    @classmethod
    def _run_callback_if_exists_hash(cls, response, hash_, callback: Callable):
        if cls.data.get(hash_, None):
            return callback()
        response.delete_cookie(key=SESSION_NAME)
        return "delete session"

    @classmethod
    def crate_session(cls, response) -> str:
        hash_: str = cls._get_hash()
        cls.data[hash_] = {"time_create": str(datetime.now())}
        response.set_cookie(key=SESSION_NAME, value=hash_)
        return hash_

    @classmethod
    def delete_session(cls, response, request) -> Optional[str]:
        hash_: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_:
            if cls.data.get(hash_, None):
                del cls.data[hash_]
            response.delete_cookie(key=SESSION_NAME)
        return hash_

    @classmethod
    def _add(cls, hash_: str, key: str, value: Any):
        cls.data[hash_][key] = value

    @classmethod
    def get(cls, request, response, key: str) -> Any:
        hash_: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_:
            return cls._run_callback_if_exists_hash(response, hash_, lambda: cls.data[hash_].get(key, None))
        return None

    @classmethod
    def keys(cls, request, response):
        hash_: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_:
            return cls._run_callback_if_exists_hash(response, hash_, lambda: list(cls.data[hash_].keys()))
        return None

    @classmethod
    def items(cls, request, response):
        hash_: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_:
            return cls._run_callback_if_exists_hash(response, hash_, lambda: cls.data[hash_])
        return None


class SESSION_FILE(SESSION_RAM):
    """
    Сессия будет взята из файла, и будет записана в файл
    после завершения сервера
    """
    file = JsonFile("session.json")

    read_fun = lambda _x: _x if _x else {}

    data = read_fun(file.readFile())

    @classmethod
    def save(cls):
        cls.file.writeFile(cls.data)


def exit_():
    """
    Сохранить данные в сессию.
    Эта функция должна быть вызвана в менеджере
    """
    SESSION_FILE.save()
