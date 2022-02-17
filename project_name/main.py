"""
Файл с главным приложением
"""
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

sys.path.append("/home/denis/PycharmProjects/fastApiProject")
from fast_xabhelper.manage import Mange
from mount import Mount

app = FastAPI(version="1.2", default_response_class=ORJSONResponse)

if __name__ == "__main__":
    mg = Mange(Mount)
    mg.main(app, "run_dev")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
