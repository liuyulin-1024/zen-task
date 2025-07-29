from fastapi import APIRouter, Body, Request

from tools.common import get_logger


router = APIRouter()
logger = get_logger()


@router.post("/login/pwd", summary="密码登录")
async def pwd_login(
    request: Request,
    phone: str = Body(),
    password: str = Body(),
):
    pass
