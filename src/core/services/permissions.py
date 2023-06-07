from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.services.authentication_service import AuthenticationService
from src.data_base.models import User


async def is_user_authenticated(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    auth_service: Annotated[AuthenticationService, Depends()]
) -> None:
    """Разрешает доступ всем аутентифицированным пользователям."""
    return await auth_service.check_current_user_exists(token=token)


async def is_administrator(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    auth_service: Annotated[AuthenticationService, Depends()]
) -> None:
    """Разрешает доступ пользователям со статусом `admin`."""
    return await auth_service.check_current_user_exists(
        token=token, statuses=[User.Status.ADMIN]
    )


async def is_administrator_or_staff(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    auth_service: Annotated[AuthenticationService, Depends()]
) -> None:
    """Разрешает доступ пользователям со статусом `staff` или `admin`."""
    return await auth_service.check_current_user_exists(
        token=token, statuses=[User.Status.ADMIN, User.Status.STAFF]
    )
