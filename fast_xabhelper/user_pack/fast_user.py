"""
# Подключить
import session_pack.fast_session

router = APIRouter()
router.include_router(user_pack.fast_user.router,
                      tags=["user"],
                      prefix="/user")
"""
from typing import Optional

from fastapi import APIRouter, Form, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fast_xabhelper.database import get_session_transaction, hashPassword, get_session
from fast_xabhelper.session_pack.session_base import SESSION
from fast_xabhelper.user_pack.uesr_model import User, regex_email

router = APIRouter(tags=["user"], prefix="/user")


def enter(response, id: int) -> str:
    hash_: str = SESSION.crate_session(response)
    SESSION.add(hash_, "user_id", id)
    return hash_


@router.post("/register")
async def register_new_user(
        response: Response,
        email: str = Form(..., regex=regex_email),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session_transaction),
):
    res = await User.register_new_user(session,
                                       email=email,
                                       hashed_password=hashPassword(password), )
    enter(response, res)
    return {"id": res}


@router.post("/create_token")
async def create_token(
        requests: Request,
        session: AsyncSession = Depends(get_session_transaction),
):
    res: str = await User.create_token(session,
                                       id_=SESSION.get(requests, 'user_id'))
    return {"token": res}


@router.get("/get_token")
async def get_token(
        requests: Request,
        session: AsyncSession = Depends(get_session_transaction),
):
    res: str = await User.get_token(session,
                                    id_=SESSION.get(requests, 'user_id'))
    return {"token": res}


@router.get("/is_login")
async def is_login(
        requests: Request,
):
    return {"id": SESSION.get(requests, 'user_id')}


@router.post("/login", tags=["user"])
async def login_user(
        response: Response,
        email: str = Form(..., regex=regex_email),
        password: str = Form(...),
        session: AsyncSession = Depends(get_session),
):
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
    return {"status": SESSION.delete_session(response, request)}
