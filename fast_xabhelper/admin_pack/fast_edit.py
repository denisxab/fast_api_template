from typing import Any

from fastapi import Request, Form, Depends, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from fast_xabhelper.admin_pack.admin_base import Admin, AdminPanel, get_tamplate, is_login_admin
from fast_xabhelper.database import get_session_transaction

router = APIRouter(prefix="/edit", tags=["admin"])


@router.post("/update", name="update_edit")
async def update_edit(
        request: Request,
        model_name: str = Form(...),
        session: AsyncSession = Depends(get_session_transaction),
        authorized: bool = Depends(is_login_admin),
):
    # Получить данные из формы
    form_: dict[str, Any] = await Admin.build_form(request)
    # Получить модель
    model: DeclarativeMeta = Admin.arr_admin[model_name].model
    # Обновить данные в таблице по id
    res = await session.execute(update(model).where(model.id == form_["id"]).values(**form_))
    # Если получилось обновить данные, вернем хеш
    if res.rowcount >= 1:
        return RedirectResponse(request.url_for("main_admin_panel", model_name=model_name))
    return {"error": "Данные не обновлены"}


@router.get("/{model_name}/{id_}", response_class=HTMLResponse, name="edit")
async def edit(
        model_name: str,
        id_: int,
        request: Request,
        templates=Depends(get_tamplate),
        authorized: bool = Depends(is_login_admin),
):
    model: AdminPanel = Admin.arr_admin[model_name]

    extend_column, title_column = model.get_colums()
    context = {"request": request,
               "model": Admin.arr_admin[model_name],
               "title_column": title_column,
               "extend_column": extend_column,
               "data_item": await model.get_row_by_id(id_),
               "url_update": request.url_for("update_edit")
               }
    return templates.TemplateResponse("edit.html", context)
