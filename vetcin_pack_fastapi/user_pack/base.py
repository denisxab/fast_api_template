from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response

from vetcin_pack_fastapi.session_pack.base import SESSION_RAM

regex_email: str = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"


def enter(response, request, id_: int) -> str:
    """
    Войти в профиль. У пользователя в сессии создается идентификатор на сайте
    """
    hash_key: str = SESSION_RAM.crate_session(response, request)
    SESSION_RAM.add(hash_key, "user_id", id_)
    return hash_key


def is_login_user(request: Request, response: Response):
    """
    Проверка авторизованно админа

    Пример использования
    @app.get("/")
    def fun(authorized: bool = Depends(is_login_admin)):
        ...
    """
    if not SESSION_RAM.get(request, response, 'user_id'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        return True
