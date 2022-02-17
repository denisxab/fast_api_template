from pathlib import Path
from typing import Optional, Any

from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from starlette.datastructures import FormData

from fast_xabhelper import convert_html_input_type_to_python_type
from fast_xabhelper.admin_pack.admin_conf import password, user
from fast_xabhelper.database import hashPassword, get_session_dec, row2dict
from fast_xabhelper.session_pack.session_base import SESSION_RAM


def get_tamplate():
    # Указываем директорию, где искать шаблоны
    return Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


def is_login_admin(request: Request, response: Response):
    """
    Проверка авторизованно админа

    Пример использования
    @app.get("/")
    def fun(authorized: bool = Depends(is_login_admin)):
        ...
    """
    if not Admin.is_login(request, response):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return True


class AdminPanel:
    # Любое имя
    name: Optional[str] = None
    # Модель `SqlAlchemy`
    model: Optional[DeclarativeMeta] = None
    # Имя столбца которые мы хотим видеть в админ панели.
    list_display: Optional[list[str]] = None

    # Указать имя столбца через которое можно перейти редактированию записи.
    # list_display_links = ("$Any2$",)
    # # Указать по каким столбцам можно делать поиск.
    # search_fields = ("$Any3$",)
    # # Столбцы которые можно редактировать не открывая всю запись.
    # list_editable = ("$Any4$",)
    # # Столбцы, по которым можно фильтровать записи.
    # list_filter = ("$Any4$",)

    @classmethod
    @get_session_dec
    async def get_rows(cls, session: AsyncSession, *args, **kwargs):
        """
        Получить все данные из таблицы
        """
        sql_ = select(cls.model)
        res = await session.execute(sql_)
        return res.fetchall()

    @classmethod
    @get_session_dec
    async def get_row_by_id(cls, id_: int, session: AsyncSession, *args, **kwargs):
        """
        Получить данные об одной записи по её ID
        """
        sql_ = select(cls.model).where(cls.model.id == id_)
        obj_ = await session.execute(sql_)
        res = obj_.first()
        if res:
            return res[0]

    @classmethod
    def get_colums(cls):
        """
        Получить столбцы
        :return:
        """
        return row2dict(cls.model, cls.list_display)


class Admin:
    # Список админ панелей
    arr_admin: dict[str, AdminPanel] = {}

    @classmethod
    def get_token(cls, Password: str, UserName: str) -> str:
        """
        Получить токен
        """
        return hashPassword(Password + UserName)

    @classmethod
    def enter(cls, response, Password: str, UserName: str) -> str:
        """
        Войти
        """
        hash_: str = SESSION_RAM.crate_session(response)
        SESSION_RAM._add(hash_, "token_admin", Admin.get_token(Password, UserName))
        return hash_

    @classmethod
    def is_login(cls, request, response):
        """
        Проверить аутентификацию
        """
        if SESSION_RAM.get(request, response, "token_admin") == cls.get_token(password, user):
            return True
        return False

    @classmethod
    def append_panel(cls, model: AdminPanel):
        """
        Добавить панель в список
        """
        cls.arr_admin[model.name] = model

    @staticmethod
    async def build_form(request) -> dict[str, Any]:
        form: FormData = await request.form()
        form: dict = form._dict
        del form["model_name"]
        res = convert_html_input_type_to_python_type(form)
        # В запросе должен быть id записи
        if res.get("id", None):
            return res
        raise KeyError("Нет ключа id. В запросе должен быть id записи")
