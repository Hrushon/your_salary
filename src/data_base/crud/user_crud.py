from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.data_base.base import get_session
from src.data_base.crud import BaseCRUD
from src.data_base.models import User


class UserCRUD(BaseCRUD):
    """Класс для реализации CRUD модели `User`."""

    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_session)]
    ) -> None:
        super().__init__(session, User)

    async def get_all(self) -> list[User | None]:
        """Возвращает список всех работников."""
        objects = await self._session.scalars(
            select(self._model)
            .options(joinedload(User.department))
            .options(joinedload(User.position))
            .options(joinedload(User.salary))
        )
        return objects.all()
