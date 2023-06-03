from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.position import PositionCreateRequest
from src.data_base.crud import PositionCRUD
from src.data_base.models import Position


class PositionsService:
    def __init__(
        self, position_crud: Annotated[PositionCRUD, Depends()]
    ) -> None:
        self._crud = position_crud

    async def get_all(self) -> list[Position]:
        """Возвращает список всех должностей из БД."""
        return await self._crud.get_all()

    async def create_position(
        self, data: PositionCreateRequest
    ) -> Position:
        """Создает должность в БД.

        Аргументы:
            data: PositionCreateRequest - данные для создания объекта.
        """
        department = Position(**data.dict())
        return await self._crud.create(department)

    async def get_by_id(
        self, obj_id: int
    ) -> Position:
        """Возвращает отдельную должность из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self._crud.get_or_404(obj_id=obj_id)

    async def update_position(
        self, obj_id: int, data: PositionCreateRequest
    ) -> Position:
        """Обновляет данные должности в БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД,
            data: PositionCreateRequest - данные для создания объекта.
        """
        data_dict = data.dict(exclude_unset=True)
        return await self._crud.update(obj_id, data_dict)

    async def delete_position(self, obj_id: int) -> None:
        """Удаляет запись с данными должности из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self._crud.delete(obj_id)
