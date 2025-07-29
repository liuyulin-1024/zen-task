import jwt

from settings import settings


async def decry_token(token: str):
    return jwt.decode(
        token,
        settings.jwt.secret_key,
        algorithms=[settings.ai_tablet.jwt.algorithm],
    )
