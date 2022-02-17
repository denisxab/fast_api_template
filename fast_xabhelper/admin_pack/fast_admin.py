from pathlib import Path

from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse

import fast_xabhelper.admin_pack.fast_login
import fast_xabhelper.admin_pack.fast_panel
from fast_xabhelper.admin_pack.admin_base import Admin
from fast_xabhelper.admin_pack.admin_conf import get_tamplate
from fast_xabhelper.helpful import add_route

router = APIRouter(prefix="/admin", tags=["admin"])

add_route(router,
          fast_xabhelper.admin_pack.fast_panel.router,
          name="panel_admin")

add_route(router,
          fast_xabhelper.admin_pack.fast_login.router,
          name="login_admin")


@router.api_route("/main", methods=["GET", "POST"], response_class=HTMLResponse, name="main_admin")
async def main_page(request: Request, templates=Depends(get_tamplate)):
    """
    Главная страница с админ панелями
    """
    context = {"request": request,
               "list_panel": []}
    for _panel in Admin.arr_admin.keys():
        context["list_panel"].append(_panel)
    return templates.TemplateResponse("index.html", context)


# Указываем что возвращаем `HTML`
@router.get("/", response_class=HTMLResponse)
def index(request: Request, response: Response, templates=Depends(get_tamplate)):
    if not Admin.is_login(request, response):
        return templates.TemplateResponse("login.html",
                                          {"request": request,
                                           "url_login": router.url_path_for("admin_login")})
    return RedirectResponse(router.url_path_for("main_admin"))
