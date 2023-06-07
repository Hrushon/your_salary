from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.department import (DepartmentCreateRequest,
                                                  DepartmentUpdateRequest)
from src.data_base.crud import DepartmentCRUD
from src.data_base.models import Department


class DepartmentService:
    def __init__(
        self, department_crud: Annotated[DepartmentCRUD, Depends()]
    ) -> None:
        self.__crud = department_crud

    async def get_all(self) -> list[Department]:
        """Возвращает список всех департаментов из БД."""
        return await self.__crud.get_all()

    async def create_department(
        self, data: DepartmentCreateRequest
    ) -> Department:
        """Создает департамент в БД.

        Аргументы:
            data: DepartmentCreateRequest - данные для создания объекта.
        """
        department = Department(**data.dict())
        return await self.__crud.create(department)

    async def get_by_id(
        self, obj_id: int
    ) -> Department:
        """Возвращает отдельный департамент из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.get_or_404(obj_id=obj_id)

    async def update_department(
        self, obj_id: int, data: DepartmentUpdateRequest
    ) -> Department:
        """Обновляет данные департамента в БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД,
            data: DepartmentUpdateRequest - данные для создания объекта.
        """
        data_dict = data.dict(exclude_unset=True)
        return await self.__crud.update(obj_id, data_dict)

    async def delete_department(self, obj_id: int) -> None:
        """Удаляет запись с данными департамента из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.delete(obj_id)
