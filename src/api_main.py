from fastapi import FastAPI, status

from .api import base_router
from .core.exc.custom_exceptions import AppBaseError
from .core.exc.exc_handlers import (application_error_handler,
                                    internal_exception_handler)
from .core.settings import settings


def create_application() -> FastAPI:
    """Создает и возвращает объект приложения FastAPI.

    Производит добавление роутеров к объекту приложения.
    """
    app = FastAPI(
        title='Your Salary ™',
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
        version=1.0,
        docs_url=settings.swagger,
        redoc_url=settings.redoc
    )
    app.include_router(base_router.router)

    app.add_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        internal_exception_handler)
    app.add_exception_handler(
        AppBaseError,
        application_error_handler
    )

    @app.on_event('startup')
    async def start_app():
        """Дополнительные действия при запуске приложения."""
        pass

    @app.on_event('shutdown')
    async def on_shutdown():
        """Дополнительные действия при остановке приложения."""
        pass

    return app
