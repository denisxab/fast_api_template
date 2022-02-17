"""
# Подключить сессию
import session_pack.fast_session

router = APIRouter()
router.include_router(session_pack.fast_session.router,
                      tags=["session"],
                      prefix="/session")
"""
from fastapi import APIRouter, Form, Response, Request

from fast_xabhelper.session_pack.session_base import SESSION

router = APIRouter(tags=["session"], prefix="/session")


@router.get("/get")
async def get_value_by_key(request: Request, key: str = Form(...), ):
    return {"value": SESSION.get(request, key)}


@router.get("/keys")
async def get_keys(response: Response, request: Request):
    return {"session": SESSION.keys(request, response)}


@router.get("/items")
async def get_items(response: Response, request: Request):
    return {"session": SESSION.items(request, response)}
