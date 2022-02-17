from pathlib import Path

from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData
from starlette.responses import RedirectResponse

from fast_xabhelper.admin_pack.admin_base import Admin
from fast_xabhelper.admin_pack.admin_conf import user, password
from fast_xabhelper.database import get_session_transaction
from fast_xabhelper.session_pack.session_base import SESSION

router = APIRouter(prefix="/admin", tags=["admin"])

# Указываем директорию, где искать шаблоны
templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


@router.post("/main", response_class=HTMLResponse, name="main_admin")
@router.get("/main", response_class=HTMLResponse, name="main_admin")
async def main_page(request: Request):
    """
    Главная страница с админ панелями
    """
    context = {"request": request,
               "list_panel": []}
    for _panel in Admin.arr_admin.keys():
        context["list_panel"].append(_panel)

    return templates.TemplateResponse("index.html", context)


@router.get("/panel/{model_name}", response_class=HTMLResponse, name="main_admin")
async def panel_model(request: Request, model_name: str):
    """
    Лента данных админ панели
    """
    model = Admin.arr_admin[model_name]
    extend_column, title_column = model.get_colums()

    context = {"request": request,
               "model": Admin.arr_admin[model_name],
               "title_column": title_column,
               "extend_column": extend_column,
               "data": await model.get_rows()
               }

    return templates.TemplateResponse("panel.html", context)


@router.post("/update", name="update_edit")
async def update_edit(request: Request,
                      model_name: str = Form(...),
                      session: AsyncSession = Depends(get_session_transaction), ):
    form: FormData = await request.form()
    form: dict = form._dict
    del form["model_name"]

    # TODO: Преобразование данные формы в данные SQL
    model = Admin.arr_admin[model_name].model
    res = await session.execute(update(model).where(model.id == form["id"]).values(**form))
    # Если получилось обновить данные, вернем хеш
    if res.rowcount > 1:
        return model_name
    return {"error": "Данные не обновлены"}


@router.get("/panel/{model_name}/edit/{id_}", response_class=HTMLResponse, name="edit")
async def edit(request: Request, model_name: str, id_: int):
    model = Admin.arr_admin[model_name]

    extend_column, title_column = model.get_colums()
    context = {"request": request,
               "model": Admin.arr_admin[model_name],
               "title_column": title_column,
               "extend_column": extend_column,
               "data_item": await model.get_row_by_id(id_),
               "url_update": router.url_path_for("update_edit")
               }
    return templates.TemplateResponse("edit.html", context)


# Указываем что возвращаем `HTML`
@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    if not Admin.is_login(request):
        return templates.TemplateResponse("login.html",
                                          {"request": request,
                                           "url_login": router.url_path_for("admin_login")})
    return RedirectResponse(router.url_path_for("main_admin"))


# Указываем что возвращаем `HTML`
@router.post("/login", name="admin_login")
def login(UserName: str = Form(...),
          Password: str = Form(...)
          ):
    response = RedirectResponse(router.url_path_for("main_admin"))
    if UserName == user and Password == password:
        Admin.enter(response, Password, UserName)
        return response
    return {"status": "False"}


@router.get("/logout")
async def logout_user(
        response: Response,
        request: Request,
):
    return {"status": SESSION.delete_session(response, request)}
