from typing import List
import ast
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import router
from api.home.home import home_router
from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
    ResponseLogMiddleware,
)

def init_routers(app_: FastAPI) -> None:
    app_.include_router(home_router)
    app_.include_router(router)

def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"success": exc.success, "message": exc.message},
        )

def on_auth_error(request: Request, exc: Exception):
    status_code, success, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        success = exc.success
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"success": success, "message": message},
    )

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware

def create_app() -> FastAPI:
    load_dotenv()
    app_ = FastAPI(
        title=os.getenv('TITLE'),
        description=os.getenv('AUTHOR'),
        version=os.getenv('VERSION'),
        docs_url=None if config.ENV == "production" else os.getenv('DOCS'),
        redoc_url=None if config.ENV == "production" else os.getenv('REDOC'),
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_

app = create_app()
