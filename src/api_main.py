from fastapi import FastAPI

from .api import base_router
from .core.settings import settings


def create_application() -> FastAPI:
    """Создает и возвращает объект приложения FastAPI.

    Производит добавление роутеров к объекту приложения.
    """
    app = FastAPI(docs_url=None, debug=settings.DEBUG)
    app.include_router(base_router.router)

    @app.on_event('startup')
    async def start_app():
        """Дополнительные действия при запуске приложения."""
        pass

    @app.on_event('shutdown')
    async def on_shutdown():
        """Дополнительные действия при остановке приложения."""
        pass

    return app
