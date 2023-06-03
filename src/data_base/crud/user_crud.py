from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_base.base import get_session
from src.data_base.crud import BaseCRUD
from src.data_base.models import User


class UserCRUD(BaseCRUD):
    """Класс для реализации CRUD модели `User`."""

    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_session)]
    ) -> None:
        super().__init__(session, User)
