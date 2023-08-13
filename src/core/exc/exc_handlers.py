from fastapi import Request, status
from fastapi.responses import JSONResponse


async def internal_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Хэндлер для ошибки `500`."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': 'Произошел внутренний сбой приложения.'},
    )


async def application_error_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Хэндлер для кастомных ошибок приложения."""
    status_code = getattr(exc, 'status_code', None)
    error_message = getattr(exc, 'detail', None)

    if status_code and error_message:
        return JSONResponse(
            status_code=status_code, content={'detail': error_message}
        )
    return await internal_exception_handler(request, exc)
