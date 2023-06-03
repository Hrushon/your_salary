from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from src.api.v1.request_models.department import (DepartmentCreateRequest,
                                                  DepartmentUpdateRequest)
from src.api.v1.response_models.department import DepartmentResponse
from src.core.services.departments_servise import DepartmentsService

router = APIRouter(
    prefix='/departments',
    tags=['Департамент'],
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Получить список всех департаментов',
    response_description='Получен список всех департаментов'
)
async def get_departments(
    service: Annotated[DepartmentsService, Depends()]
) -> list[DepartmentResponse]:
    """
    Возвращает список всех департаментов из базы данных.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название департамента
    - **employees**: список работников департамента
    """
    return await service.get_all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Создать департамент в БД',
    response_description='Создан департамент в БД'
)
async def create_departament(
    data: DepartmentCreateRequest,
    service: Annotated[DepartmentsService, Depends()],
) -> DepartmentResponse:
    """
    Создает запись нового департамента в базе данных.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название департамента
    - **employees**: список работников департамента
    """
    return await service.create_department(data=data)


@router.get(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Получить данные отдельного департамента из БД',
    response_description='Получены данные департамента из БД'
)
async def get_departament_by_id(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[DepartmentsService, Depends()],
) -> DepartmentResponse:
    """
    Возвращает запись отдельного департамента из базы данных по полю `id`.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название департамента
    - **employees**: список работников департамента
    """
    return await service.get_by_id(obj_id=obj_id)


@router.patch(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Обновить данные департамента в БД',
    response_description='Обновленны данные департамента в БД'
)
async def update_departament(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: DepartmentUpdateRequest,
    service: Annotated[DepartmentsService, Depends()],
) -> DepartmentResponse:
    """
    Обновляет запись отдельного департамента в базы данных по полю `id`.

    И возвращает данные обновленного департамента.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название департамента
    - **employees**: список работников департамента
    """
    return await service.update_department(obj_id=obj_id, data=data)


@router.delete(
    '/{obj_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить данные департамента из БД',
    response_description='Удалены данные департамента из БД'
)
async def delete_departament(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[DepartmentsService, Depends()],
) -> None:
    """Удаляет запись отдельного департамента из базы данных по полю `id`."""
    return await service.delete_department(obj_id=obj_id)
