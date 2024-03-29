from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.position import (PositionCreateRequest,
                                                PositionUpdateRequest)
from src.data_base.crud import PositionCRUD
from src.data_base.models import Position


class PositionService:
    def __init__(
        self, position_crud: Annotated[PositionCRUD, Depends()]
    ) -> None:
        self.__crud = position_crud

    async def get_all(self) -> list[Position]:
        """Возвращает список всех должностей из БД."""
        return await self.__crud.get_all()

    async def create_position(
        self, data: PositionCreateRequest
    ) -> Position:
        """Создает должность в БД.

        Аргументы:
            data: PositionCreateRequest - данные для создания объекта.
        """
        position = Position(**data.dict())
        return await self.__crud.create(position)

    async def get_by_id(
        self, obj_id: int
    ) -> Position:
        """Возвращает отдельную должность из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.get_or_404(obj_id=obj_id)

    async def update_position(
        self, obj_id: int, data: PositionUpdateRequest
    ) -> Position:
        """Обновляет данные должности в БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД,
            data: PositionUpdateRequest - данные для создания объекта.
        """
        data_dict = data.dict(exclude_unset=True)
        return await self.__crud.update(obj_id, data_dict)

    async def delete_position(self, obj_id: int) -> None:
        """Удаляет запись с данными должности из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.delete(obj_id)
