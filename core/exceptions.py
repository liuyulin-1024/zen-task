from fastapi import status
from starlette.requests import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.authentication import AuthenticationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class ValidationException(Exception):
    """参数校验失败"""


class ServerException(Exception):
    """服务器错误"""


class PermissionException(Exception):
    """无权限操作"""


class NotFoundException(Exception):
    """数据未找到"""


class OfflineException(Exception):
    """设备不在线"""


def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {"code": status.HTTP_400_BAD_REQUEST, "message": str(exc.args[0])}
        ),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {"code": status.HTTP_400_BAD_REQUEST, "message": str(exc.detail)}
        ),
    )


def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    # 兼容登录依赖的报错
    try:
        if "authorization" in exc.args[0][0]["loc"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": "用户认证失败",
                    }
                ),
            )
    except (IndexError, KeyError):
        pass

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": f"请检查输入的参数！{exc}",
            }
        ),
    )


def server_exception_handler(request: Request, exc: ServerException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(exc.args[0])}
        ),
    )


def permission_exception_handler(request: Request, exc: ServerException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {"code": status.HTTP_400_BAD_REQUEST, "message": str(exc.args[0])}
        ),
    )


def authentication_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": str(exc),
            }
        ),
    )


def notfound_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "code": status.HTTP_404_NOT_FOUND,
                "message": str(exc),
            }
        ),
    )


def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"服务器异常：{exc}",
            }
        ),
    )


exception_handlers = {
    AuthenticationError: authentication_exception_handler,
    StarletteHTTPException: http_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    ValidationException: validation_exception_handler,
    ServerException: server_exception_handler,
    PermissionException: permission_exception_handler,
    NotFoundException: notfound_exception_handler,
    Exception: global_exception_handler,
}
