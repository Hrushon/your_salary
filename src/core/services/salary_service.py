from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.salary import (SalaryCreateRequest,
                                              SalaryUpdateRequest)
from src.data_base.crud import SalaryCRUD
from src.data_base.models import Salary


class SalaryService:
    def __init__(
        self, salary_crud: Annotated[SalaryCRUD, Depends()]
    ) -> None:
        self.__crud = salary_crud

    async def get_all(self) -> list[Salary]:
        """Возвращает список всех заработных плат из БД."""
        return await self.__crud.get_all()

    async def create_salary(
        self, data: SalaryCreateRequest
    ) -> Salary:
        """Создает запись с заработной платой в БД.

        Аргументы:
            data: SalaryCreateRequest - данные для создания объекта.
        """
        salary = Salary(**data.dict())
        return await self.__crud.create(salary)

    async def get_by_id(
        self, obj_id: int
    ) -> Salary:
        """Возвращает отдельную запись с заработной платой из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.get_or_404(obj_id=obj_id)

    async def update_salary(
        self, obj_id: int, data: SalaryUpdateRequest
    ) -> Salary:
        """Обновляет данные записи с заработной платой в БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД,
            data: SalaryUpdateRequest - данные для создания объекта.
        """
        data_dict = data.dict(exclude_unset=True)
        return await self.__crud.update(obj_id, data_dict)

    async def delete_salary(self, obj_id: int) -> None:
        """Удаляет запись с данными заработной платы из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.delete(obj_id)
