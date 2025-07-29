import traceback

import jwt
from fastapi import Request
from starlette.authentication import AuthenticationError

from core.models import User
from tools.common import get_logger
from api.users.services import decry_token


logger = get_logger()


async def authentication(request: Request) -> User:
    authorization = request.headers.get("Authorization", "")
    if not authorization:
        raise AuthenticationError("用户认证失败")

    try:
        slogan, token = authorization.split()
        data = await decry_token(token)
        user_id = data.get("data", {}).get("id")
        user_instance = await User.filter(id=user_id).first()
        if not user_instance:
            raise AuthenticationError("用户认证失败")
    except ValueError:
        raise AuthenticationError("token已失效！")
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("token已过期！")
    except jwt.InvalidTokenError:
        raise AuthenticationError("token已失效！")
    except Exception:
        logger.error(f"Failed authorization: {traceback.format_exc()} {authorization}")
        raise AuthenticationError("用户认证失败")

    return user_instance

