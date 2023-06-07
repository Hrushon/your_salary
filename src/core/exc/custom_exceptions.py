from typing import TypeVar

from fastapi import status

from src.data_base.models import User

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


class ForbiddenError(AppBaseError):
    status_code: status = status.HTTP_403_FORBIDDEN
    detail = "У вас недостаточно прав для выполнения этой операции"


class UnauthorizedError(AppBaseError):
    status_code: status = status.HTTP_401_UNAUTHORIZED
    detail = "У Вас нет прав для просмотра запрошенной страницы."


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


class UserNotFoundError(NotFoundError):
    detail: str = 'Работник с данными реквизатами не найден'


class UserBlockedError(ForbiddenError):
    detail: str = 'Профиль работника заблокирован'


class InvalidAuthenticationDataError(BadRequestError):
    detail = "Неверный `username` или пароль."


class UserUnknownStatusError(BadRequestError):
    def __init__(self, status: User.Status) -> None:
        self.detail = 'Неизвестный пользовательский статус {}'.format(
            status
        )
