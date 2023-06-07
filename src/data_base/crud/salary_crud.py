from typing import Annotated

from fastapi import Depends
from pydantic import FutureDate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_base.base import get_session
from src.data_base.crud import BaseCRUD
from src.data_base.models import Salary


class SalaryCRUD(BaseCRUD):
    """Класс для реализации CRUD модели `Salary`."""

    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_session)]
    ) -> None:
        super().__init__(session, Salary)

    async def get_all(
        self,
        date_after: FutureDate | None = None,
        date_before: FutureDate | None = None
    ) -> list[Salary | None]:
        """Возвращает список всех объектов модели.

        При получении аргументов `date_before`, `date_after` -
        фильтрует результаты запросов по этим датам.
        """
        query = select(self._model)
        if date_after:
            query = query.filter(self._model.raise_date >= date_after)
        if date_before:
            query = query.filter(self._model.raise_date <= date_before)
        objects = await self._session.scalars(query)
        return objects.unique().all()
