from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse

import fast_xabhelper.admin_pack.fast_login
import fast_xabhelper.admin_pack.fast_panel
from fast_xabhelper.admin_pack.admin_base import Admin, get_tamplate, is_login_admin
from fast_xabhelper.mount_logic import BaseMount

router = APIRouter(prefix="/admin", tags=["admin"])

BaseMount.add_route(router,
                    fast_xabhelper.admin_pack.fast_panel.router,
                    name="panel_admin")

BaseMount.add_route(router,
                    fast_xabhelper.admin_pack.fast_login.router,
                    name="login_admin")


@router.api_route("/main",
                  methods=["GET", "POST"],
                  include_in_schema=False,
                  response_class=HTMLResponse,
                  name="main_admin")
async def main_page(
        request: Request,
        templates=Depends(get_tamplate),
        authorized: bool = Depends(is_login_admin),
):
    """
    Главная страница с админ панелями
    """
    context = {"request": request,
               "list_panel": []}
    for _panel in Admin.arr_admin.keys():
        context["list_panel"].append(_panel)
    return templates.TemplateResponse("indexs.html", context)


# Указываем что возвращаем `HTML`
@router.get("/",
            response_class=HTMLResponse,
            include_in_schema=False,
            name="index_admin")
def index(
        request: Request,
        response: Response,
        templates=Depends(get_tamplate)
):
    if not Admin.is_login(request, response):
        # TODO: login.html
        return templates.TemplateResponse("index.html", {"request": request})
        # return templates.TemplateResponse("login.html",
        #                                   {"request": request,
        #                                    "url_login": router.url_path_for("admin_login")})
    return RedirectResponse(router.url_path_for("main_admin"))
