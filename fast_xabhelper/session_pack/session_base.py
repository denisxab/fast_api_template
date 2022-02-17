from datetime import datetime
from typing import Any, Optional

from fast_xabhelper.database import hashRandom


# Хранилище сессий
class SESSION:
    data: dict[str, Any] = {}

    @classmethod
    def __get_hash(cls) -> str:
        return hashRandom()

    @classmethod
    def crate_session(cls, response) -> str:
        hash_ = cls.__get_hash()
        cls.data[hash_] = {"time_create": datetime.now()}
        response.set_cookie(key="session_id", value=hash_)
        return hash_

    @classmethod
    def delete_session(cls, response, request) -> Optional[str]:
        hash_: Optional[str] = request.cookies.get("session_id", None)
        if hash_:
            if cls.data.get(hash_, None):
                del cls.data[hash_]
            response.delete_cookie(key="session_id")
        return hash_

    @classmethod
    def add(cls, hash_: str, key: str, value: Any):
        cls.data[hash_][key] = value

    @classmethod
    def get(cls, request, key: str) -> Any:
        hash_: Optional[str] = request.cookies.get("session_id", None)
        if hash_:
            if cls.data.get(hash_, None):
                return cls.data[hash_].get(key, None)
        return None

    @classmethod
    def keys(cls, request, response):
        hash_: Optional[str] = request.cookies.get("session_id", None)
        if hash_:
            if cls.data.get(hash_, None):
                return list(cls.data[hash_].keys())
            response.delete_cookie(key="session_id")
            return "delete session"
        return None

    @classmethod
    def items(cls, request, response):
        hash_: Optional[str] = request.cookies.get("session_id", None)
        if hash_:
            if cls.data.get(hash_, None):
                return cls.data[hash_]
            response.delete_cookie(key="session_id")
            return "delete session"
        return None
