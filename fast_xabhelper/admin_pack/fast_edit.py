from fastapi import Request, Form, Depends, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData

# from fast_admin import router, templates
from fast_xabhelper.admin_pack.admin_base import Admin
from fast_xabhelper.admin_pack.admin_conf import get_tamplate
from fast_xabhelper.database import get_session_transaction

router = APIRouter(prefix="/edit", tags=["admin"])


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


@router.get("/{model_name}/{id_}", response_class=HTMLResponse, name="edit")
async def edit(request: Request, model_name: str, id_: int, templates=Depends(get_tamplate)):
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
