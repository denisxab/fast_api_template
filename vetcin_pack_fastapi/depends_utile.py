"""
Файл для зависимостей в функциях
"""

import os.path

from fastapi.templating import Jinja2Templates


def get_template(name_app: str = ''):
    """
    Подключение папки с шаблонами

    :Пример подключения:

    ..code-block::python

        from fastapi import APIRouter, Request, Depends
        from starlette.responses import HTMLResponse

        from vetcin_pack_fastapi.depends_utile import get_template

        router = APIRouter(tags=["base_app"], prefix="/base_app")
        name_app = 'ИмяПриложения'

        @router.get('/', response_class=HTMLResponse)
        def index_fun(request: Request, templates=Depends(lambda: get_template(name_app))):
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                }
            )
    """
    # Указываем директорию, где искать шаблоны
    return Jinja2Templates(directory=os.path.join(name_app, "templates"))
