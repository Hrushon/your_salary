from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exc import custom_exceptions
from src.data_base.base import get_session
from src.data_base.crud import BaseCRUD
from src.data_base.models import User


class UserCRUD(BaseCRUD):
    """Класс для реализации CRUD модели `User`."""

    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_session)]
    ) -> None:
        super().__init__(session, User)

    async def get_by_username(self, username: str) -> User:
        """Получает из БД работника по его `username`.

        В случае отсутствия бросает ошибку.

        Аргументы:
            username: str - никнейм/логин работника.
        """
        user = await self._session.scalars(
            select(self._model).where(self._model.username == username)
        )
        user = user.first()
        if not user:
            raise custom_exceptions.UserNotFoundError
        return user

    async def is_user_exists(
        self, username: str, status: User.Status | None = None
    ) -> bool:
        """Проверяет существование записи пользователя в БД.

        Аргументы:
            username: str - никнейм/логин пользователя
            status: User.Status - статус пользователя
        """
        user_exists = await self._session.scalars(select(
            select(self._model).where(
                (self._model.username == username)
                & (status is None)
                | (self._model.status == status)
            ).exists()
        ))
        return user_exists.first()
