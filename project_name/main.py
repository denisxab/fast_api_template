import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import api
import static_pack.static_logic

app = FastAPI(version="1.2", default_response_class=ORJSONResponse)

app.include_router(api.router, prefix="/api")
app.include_router(static_pack.static_logic.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
