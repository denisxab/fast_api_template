"""
Файл с главным приложением
"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from mg_file.file.base_file import concat_absolute_dir_path

from fast_xabhelper.manage_logic import Mange, comd
from settings import Mount

app = FastAPI(version="1.2", default_response_class=ORJSONResponse)

mg = Mange(Mount, app, path_settings=concat_absolute_dir_path(__file__, "settings.py"))
mg.run_command(comd.init_app)
