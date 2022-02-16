from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()
router.mount(
    # `URL` путь
    "/static",
    # Директория в которой искать статические файлы
    StaticFiles(directory="./static_pack/static"),
    # Это имя будем использовать в
    # `{{ url_for('$name$', path='/$Файл$.css') ) }}`
    name="static")

# Указываем директорию, где искать шаблоны
templates = Jinja2Templates(directory="templates")
