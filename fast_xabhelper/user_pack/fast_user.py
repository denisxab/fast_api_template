"""
API для работы с пользователем
# Подключить
import session_pack.fast_session

router = APIRouter()
router.include_router(user_pack.fast_user.router)
"""

from typing import Optional

from fastapi import APIRouter, Form, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fast_xabhelper.database_pack.database import get_session_transaction, get_session
from fast_xabhelper.database_pack.db_helper import hashPassword
from fast_xabhelper.session_pack.session_base import SESSION_RAM
from fast_xabhelper.user_pack.model import User, regex_email

router = APIRouter(tags=["user"], prefix="/user")


def enter(response, id_: int) -> str:
    """Войти"""
    hash_: str = SESSION_RAM.crate_session(response)
    SESSION_RAM._add(hash_, "user_id", id_)
    return hash_


@router.post("/register")
async def register(
        response: Response,
        email: str = Form(..., regex=regex_email),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session_transaction),
):
    """Зарегистрировать нового пользователя"""
    res = await User.register(session,
                              email=email,
                              hashed_password=hashPassword(password))
    if res:
        # Войти в профиль
        enter(response, res)
        return {"id": res}
    return {"error": "Ошибка регистрации"}


@router.post("/create_token")
async def create_token(
        requests: Request,
        session: AsyncSession = Depends(get_session_transaction),
):
    """Создать токен для своего пользователя"""
    res: str = await User.create_token(session,
                                       id_=SESSION_RAM.get(requests, 'user_id'))
    return {"token": res}


@router.get("/get_token")
async def get_token(
        requests: Request,
        session: AsyncSession = Depends(get_session_transaction),
):
    """Получить свой токен пользователя"""
    res: str = await User.get_token(session,
                                    id_=SESSION_RAM.get(requests, 'user_id'))
    return {"token": res}


@router.get("/is_login")
async def is_login(
        requests: Request,
):
    """Проверить аутентификацию"""
    return {"id": SESSION_RAM.get(requests, 'user_id')}


@router.post("/login", tags=["user"])
async def login_user(
        response: Response,
        email: str = Form(..., regex=regex_email),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session),
):
    """Войти в аккаунт пользователя"""
    res_id: Optional[User] = await User.login_user(session,
                                                   email=email,
                                                   hashed_password=hashPassword(password))
    if res_id:
        return {"id": res_id, "hash_": enter(response, res_id)}
    return {"error": "Пользователь не найден"}


@router.get("/logout", tags=["user"])
async def logout_user(
        response: Response,
        request: Request,
):
    """Выйти из аккаунта пользователя"""
    return {"status": SESSION_RAM.delete_session(response, request)}
