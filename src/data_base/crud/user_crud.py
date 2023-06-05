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
        self, username: str, statuses: list[User.Status] | None = None
    ) -> bool:
        """Проверяет существование записи пользователя в БД.

        Аргументы:
            username: str - никнейм/логин пользователя
            statuses: list[User.Status] - список статусов пользователя
        """
        query = select(self._model).where(self._model.username == username)
        if statuses:
            query = query.where(self._model.status.in_(statuses))
        user_exists = await self._session.scalars(select(query.exists()))
        return user_exists.first()

    async def update_by_obj(self, obj: User, data: dict | None = None) -> User:
        """Обновляет данные полученного объекта модели в БД.

        Аргументы:
            obj: User - объект данных пользователя
            data: dict - данные пользователя
        """
        if data:
            for key, value in data.items():
                setattr(obj, key, value)
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj
