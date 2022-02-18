from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse

import fast_xabhelper.admin_pack.fast_edit
import fast_xabhelper.admin_pack.fast_edit
from fast_xabhelper.admin_pack.admin_base import Admin, get_tamplate, is_login_admin
from fast_xabhelper.helpful import add_route

router = APIRouter(prefix="/panel", tags=["admin"])

add_route(router,
          fast_xabhelper.admin_pack.fast_edit.router,
          name="edit_admin")


@router.api_route("/{model_name}",
                  methods=["GET", "POST"],
                  response_class=HTMLResponse,
                  name="main_admin_panel")
async def panel_model(
        request: Request, model_name: str,
        authorized: bool = Depends(is_login_admin),
        templates=Depends(get_tamplate)
):
    """
    Лента данных админ панели
    """
    model = Admin.arr_admin[model_name]
    extend_column, title_column = model.get_colums()
    context = {"request": request,
               "model": Admin.arr_admin[model_name],
               "title_column": title_column,
               "extend_column": extend_column,
               "data": await model.get_rows(),
               "url_lambda": lambda data:
               request.url_for("edit", model_name=model.name, id_=data),
               "url_create": request.url_for("create_model_which_admin_panel", model_name=model_name),
               }
    return templates.TemplateResponse("panel.html", context)
