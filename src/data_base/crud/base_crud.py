from abc import ABC
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import custom_exceptions

ModelType = TypeVar('ModelType')


class BaseCRUD(ABC):
    """Базовый класс для реализации CRUD-операций."""

    def __init__(self, session: AsyncSession, model: ModelType) -> None:
        self._session = session
        self._model = model

    async def get_or_none(self, obj_id: int) -> ModelType | None:
        """Возвращает объект модели из БД по `id` или `None`."""
        return await self._session.get(self._model, obj_id)

    async def get_or_404(self, obj_id: int) -> ModelType | None:
        """Возвращает объект модели из БД `id` или ошибку `404`."""
        obj = await self.get_or_none(obj_id=obj_id)
        if not obj:
            raise custom_exceptions.ObjectNotExistError(
                model=self._model, obj_id=obj_id
            )
        return obj

    async def get_all(self) -> list[ModelType | None]:
        """Возвращает список всех объектов модели."""
        objects = await self._session.scalars(select(self._model))
        return objects.all()

    async def create(self, instance: ModelType) -> ModelType:
        """Создает объект модели и сохраняет в БД."""
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError: # noqa
            raise custom_exceptions.ObjectAlreadyExistError(instance)

        await self._session.refresh(instance)
        return instance

    async def update(self, obj_id: int, data: dict) -> ModelType:
        """Обновляет данные объекта модели в БД."""
        obj = await self.get_or_404(obj_id=obj_id)
        for key, value in data.items():
            setattr(obj, key, value)
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> None:
        """Удаляет объект модели из БД по `id`."""
        obj = await self.get_or_404(obj_id=obj_id)
        await self._session.delete(obj)
        await self._session.commit()
