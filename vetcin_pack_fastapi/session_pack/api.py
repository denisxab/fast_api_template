"""
# Подключить сессию
import session_pack.fast_session

router = APIRouter()
router.include_router(session_pack.fast_session.router,
                      tags=["session"],
                      prefix="/session")
"""
from fastapi import APIRouter, Form, Response, Request

from vetcin_pack_fastapi.session_pack.base import SESSION_RAM

router = APIRouter(tags=["session"], prefix="/session")


@router.get("/get")
async def get_value_by_key(response: Response, request: Request, key: str = Form(...), ):
    return {"value": SESSION_RAM.get(request, response, key)}


@router.get("/keys")
async def response_keys(response: Response, request: Request):
    return {"session": SESSION_RAM.keys(request, response)}


@router.get("/items")
async def response_items(response: Response, request: Request):
    return {"session": SESSION_RAM.items(request, response)}
