from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from src.api.v1.request_models.position import (PositionCreateRequest,
                                                PositionUpdateRequest)
from src.api.v1.response_models.error import generate_error_responses
from src.api.v1.response_models.position import PositionResponse
from src.core.services.permissions import is_administrator_or_staff
from src.core.services.position_service import PositionService

router = APIRouter(
    prefix='/positions',
    tags=['Должности'],
    dependencies=(Depends(is_administrator_or_staff),)
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Получить список всех должностей',
    response_description='Получен список всех должностей'
)
async def get_positions(
    service: Annotated[PositionService, Depends()]
) -> list[PositionResponse]:
    """
    Возвращает список всех должностей из базы данных.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название должности
    - **employees**: список работников с этой должностью
    """
    return await service.get_all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Создать должность в БД',
    response_description='Создана должность в БД',
    responses=generate_error_responses(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def create_position(
    data: PositionCreateRequest,
    service: Annotated[PositionService, Depends()],
) -> PositionResponse:
    """
    Создает запись новой должности в базе данных.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название должности
    """
    return await service.create_position(data=data)


@router.get(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Получить данные отдельной должности из БД',
    response_description='Получены данные должности из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def get_position_by_id(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[PositionService, Depends()],
) -> PositionResponse:
    """
    Возвращает запись отдельной должности из базы данных по полю `id`.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название должности
    - **employees**: список работников с этой должностью
    """
    return await service.get_by_id(obj_id=obj_id)


@router.patch(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Обновить данные должности в БД',
    response_description='Обновлены данные должности в БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def update_position(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: PositionUpdateRequest,
    service: Annotated[PositionService, Depends()],
) -> PositionResponse:
    """
    Обновляет запись отдельной должности в базе данных по полю `id`.

    И возвращает данные обновленного департамента.

    - **id**: уникальный идентификатор записи в БД
    - **title**: название должности
    """
    return await service.update_position(obj_id=obj_id, data=data)


@router.delete(
    '/{obj_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить данные должности из БД',
    response_description='Удалены данные должности из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def delete_position(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[PositionService, Depends()],
) -> None:
    """Удаляет запись отдельной должности из базы данных по полю `id`."""
    return await service.delete_position(obj_id=obj_id)
