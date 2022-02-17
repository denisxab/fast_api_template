from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import fast_xabhelper.session_pack.fast_session
import fast_xabhelper.user_pack.fast_user
from admin import UserPanel
from fast_xabhelper.admin_pack.admin_base import Admin
from fast_xabhelper.database import get_session_transaction
from fast_xabhelper.user_pack.uesr_model import User

router = APIRouter(prefix="/api")

router.include_router(fast_xabhelper.session_pack.fast_session.router, )
router.include_router(fast_xabhelper.user_pack.fast_user.router, )

# Добавить настройки
Admin.append_panel(UserPanel())


@router.post("/main")
async def index(session: AsyncSession = Depends(get_session_transaction)):
    sql_ = User(email='SSSsdssDDDda@asd.com', hashed_password="1dafqf2f", is_active=False)
    session.add(sql_)
    await session.commit()
    return "@"
