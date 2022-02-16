from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import session_pack.fast_session
import user_pack.fast_user
from database import get_session_transaction
from user_pack.uesr_model import User

router = APIRouter()

router.include_router(session_pack.fast_session.router,
                      tags=["session"],
                      prefix="/session")
router.include_router(user_pack.fast_user.router,
                      tags=["user"],
                      prefix="/user")


@router.post("/main")
async def index(session: AsyncSession = Depends(get_session_transaction)):
    sql_ = User(email='SSSsdssDDDda@asd.com', hashed_password="1dafqf2f", is_active=False)
    session.add(sql_)
    await session.commit()
    return "@"
