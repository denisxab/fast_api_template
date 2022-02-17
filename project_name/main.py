"""
Файл с главным приложением
"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fast_xabhelper.manage import Mange
from mount import Mount

app = FastAPI(version="1.2", default_response_class=ORJSONResponse)

mg = Mange(Mount, app)
mg.main("init")

if __name__ == "__main__":
    mg.main("run_dev")
