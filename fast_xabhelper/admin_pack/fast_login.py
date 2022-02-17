from fastapi import Request, Form, Response, APIRouter
from starlette.responses import RedirectResponse

import fast_xabhelper.admin_pack.fast_admin
from fast_xabhelper.admin_pack.admin_base import Admin
from fast_xabhelper.admin_pack.admin_conf import user, password
from fast_xabhelper.session_pack.session_base import SESSION_RAM

router = APIRouter(prefix="/user", tags=["admin"])


# Указываем что возвращаем `HTML`
@router.post("/login", name="admin_login")
def login(UserName: str = Form(...), Password: str = Form(...)):
    response = RedirectResponse(fast_xabhelper.admin_pack.fast_admin.router.url_path_for("main_admin"))
    if UserName == user and Password == password:
        Admin.enter(response, Password, UserName)
        return response
    return {"status": "False"}


@router.get("/logout")
async def logout_user(response: Response, request: Request):
    return {"status": SESSION_RAM.delete_session(response, request)}
