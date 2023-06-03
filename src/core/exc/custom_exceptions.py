from typing import TypeVar

from fastapi import status

ModelType = TypeVar('ModelType')


class AppBaseError(Exception):
    """Базовое исключение приложения."""

    detail: str = 'Что-то пошло не так!'


class BadRequestError(AppBaseError):
    status_code: status = status.HTTP_400_BAD_REQUEST
    detail: str = 'Неверный запрос'


class NotFoundError(AppBaseError):
    status_code: status = status.HTTP_404_NOT_FOUND
    detail: str = 'Объект не найден'


class ObjectNotExistError(NotFoundError):
    def __init__(self, model: ModelType, obj_id: int) -> None:
        self.detail = 'Объект {} с id {} не найден'.format(
            model.__name__, obj_id
        )


class ObjectAlreadyExistError(BadRequestError):
    def __init__(self, model: ModelType) -> None:
        self.detail = 'Данный объект модели {} уже существует'.format(
            model.__name__
        )
