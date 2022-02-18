from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response

from fast_xabhelper.session_pack.session_base import SESSION_RAM


def enter(response, id_: int) -> str:
    """Войти"""
    hash_: str = SESSION_RAM.crate_session(response)
    SESSION_RAM._add(hash_, "user_id", id_)
    return hash_


def is_login_user(request: Request, response: Response):
    """
    Проверка авторизованно админа

    Пример использования
    @app.get("/")
    def fun(authorized: bool = Depends(is_login_admin)):
        ...
    """

    if not SESSION_RAM.get(request, response, 'user_id'):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return True
