import os
import sys
import asyncio
from asyncio import Queue as AsyncQueue
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise
from hypercorn.asyncio import serve
from hypercorn.config import Config
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from core.exceptions import exception_handlers
from core.registers import register_routers
from tools.common import get_logger
from settings import env, settings


loop = asyncio.get_event_loop()
diamond_queue = AsyncQueue()
logger = get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # ################## before the app starts ##################
    logger.info(f"ZenTask Server {env} Start...")

    # await Tortoise.init(settings.database.to_dict())
    await register_routers()

    yield

    # ################## before the app closes ##################
    await Tortoise.close_connections()


app = FastAPI(
    title="ZenTask",
    lifespan=lifespan,
    docs_url=settings.app.docs_url,
    redoc_url=settings.app.redoc_url,
    exception_handlers=exception_handlers,
)

register_tortoise(
    app,
    settings.database.to_dict(),
    generate_schemas=False,
    add_exception_handlers=True,
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(serve(app, config))