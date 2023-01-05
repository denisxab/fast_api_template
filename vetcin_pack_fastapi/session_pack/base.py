"""
Файл для работы с сессиями
"""
from abc import abstractclassmethod
from datetime import datetime
from typing import Any, Optional, Callable

from mg_sql.sql_async.helpful import hashPassword, hashRandom

SESSION_NAME = "session_id"


class SESSION:
    data: dict[str, Any] = {}

    @classmethod
    def _get_hash(cls) -> str:
        return hashRandom()

    @abstractclassmethod
    def _run_callback_if_exists_hash(cls, response, hash_key, callback: Callable):
        """Выполнить функцию `callback` если хеш верный"""
        ...

    @classmethod
    def crate_session(cls, response, request) -> str:
        """Создать сессию, Если она уже существует то создастся новая сессия"""
        # Если сессии нет
        if not request.cookies.get(SESSION_NAME):
            # Создаем её
            cls._crate_session(response, request)
        # Если сессия есть
        else:
            # Удаляем сессию и создаем её заново
            cls._delete_session(response, request)
            return cls._crate_session(response, request)

    @abstractclassmethod
    def _crate_session(cls, response, request) -> str:
        """Создать сессию"""
        ...

    @abstractclassmethod
    def _delete_session(cls, response, request) -> Optional[str]:
        """Удалить сессию"""
        ...

    @abstractclassmethod
    def add(cls, hash_key: str, key: str, value: Any):
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
    """Сессия в ОЗУ"""

    @classmethod
    def _run_callback_if_exists_hash(cls, response, hash_key, callback: Callable):
        if cls.data.get(hash_key, None):
            return callback()
        # Если хеш не верный, то удалить сессию из запроса
        response.delete_cookie(key=SESSION_NAME)
        return False

    @classmethod
    def _crate_session(cls, response, request) -> str:
        hash_key: str = cls._get_hash()
        cls.data[hash_key] = {"time_create": str(datetime.now())}
        response.set_cookie(key=SESSION_NAME, value=hash_key)
        return hash_key

    @classmethod
    def _delete_session(cls, response, request) -> Optional[str]:
        hash_key: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_key:
            # Удаляем куки из базы сервера
            if cls.data.get(hash_key, None):
                del cls.data[hash_key]
            # Просим удалить куки на стороне клиента
            response.delete_cookie(key=SESSION_NAME)
            # Удаляем куки из запроса клиента
            del request.cookies[SESSION_NAME]
        return hash_key

    @classmethod
    def add(cls, hash_key: str, key: str, value: Any):
        cls.data[hash_key][key] = value

    @classmethod
    def get(cls, request, response, key: str) -> Any:
        hash_key: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_key:
            return cls._run_callback_if_exists_hash(response, hash_key, lambda: cls.data[hash_key].get(key, None))
        return None

    @classmethod
    def keys(cls, request, response):
        hash_key: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_key:
            return cls._run_callback_if_exists_hash(response, hash_key, lambda: list(cls.data[hash_key].keys()))
        return None

    @classmethod
    def items(cls, request, response):
        hash_key: Optional[str] = request.cookies.get(SESSION_NAME, None)
        if hash_key:
            return cls._run_callback_if_exists_hash(response, hash_key, lambda: cls.data[hash_key])
        return None

# class SESSION_FILE(SESSION_RAM):
#     """
#     Сессия будет взята из файла, и будет записана в файл
#     после завершения сервера
#     """
#     file = JsonFile(path.join(environ["BASE_DIR"], "session.json"))
#
#     read_fun = lambda _x: _x if _x else {}
#
#     data = read_fun(file.readFile())
#
#     @classmethod
#     def save(cls):
#         """
#         Сохранить данные из сессии в файл
#         """
#         cls.file.writeFile(cls.data)

# def exit_session():
#     """
#     Сохранить данные в сессию.
#     Эта функция должна быть вызвана в менеджере
#     """
#     SESSION_FILE.save()
