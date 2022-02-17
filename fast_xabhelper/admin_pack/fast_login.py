from fastapi import Request, Form, Response, APIRouter, Depends
from starlette.responses import RedirectResponse

import fast_xabhelper.admin_pack.fast_admin
from fast_xabhelper.admin_pack.admin_base import Admin, is_login_admin, ADMIN_PASSWORD, ADMIN_USER_NAME
from fast_xabhelper.session_pack.session_base import SESSION_RAM

router = APIRouter(prefix="/user", tags=["admin"])


# Указываем что возвращаем `HTML`
@router.post("/login", name="admin_login")
def login(UserName: str = Form(...), Password: str = Form(...)):
    response = RedirectResponse(fast_xabhelper.admin_pack.fast_admin.router.url_path_for("main_admin"))
    if UserName == ADMIN_USER_NAME and Password == ADMIN_PASSWORD:
        Admin.enter(response, Password, UserName)
        return response
    return {"status": "False"}


@router.get("/logout")
async def logout(
        response: Response,
        request: Request,
        authorized: bool = Depends(is_login_admin),
):
    return {"status": SESSION_RAM.delete_session(response, request)}
