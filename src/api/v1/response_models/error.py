from typing import Any

from fastapi import status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str = 'Текст ошибки'


def generate_error_responses(
    *error_statuses: status
) -> dict[int, dict[str, Any]]:
    """Создает схемы ошибок из входящих статус-кодов."""
    return {
        error_status.real: {
            'model': ErrorResponse
        } for error_status in error_statuses
    }
