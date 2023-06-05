from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.api.v1.request_models.user import UserAuthenticateRequest
from src.api.v1.response_models.user import UserResponse
from src.core.exc import custom_exceptions
from src.core.settings import settings
from src.data_base.crud import UserCRUD
from src.data_base.DTO_models import UserAndTokenDTO
from src.data_base.models import User

ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
PASSWORD_CONTEXT: CryptContext = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


class AuthenticationService:
    def __init__(
        self,
        user_crud: Annotated[UserCRUD, Depends()]
    ) -> None:
        self.__crud = user_crud

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширует пароль."""
        return PASSWORD_CONTEXT.hash(password)

    @staticmethod
    def get_username_from_token(token: str) -> str:
        """Декодирует JWT-токен и возвращает `username`.

        Аргументы:
            token: str - JWT-токен
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[ALGORITHM]
            )
        except JWTError:
            raise custom_exceptions.UnauthorizedError
        username = payload.get('username')
        if not username:
            raise custom_exceptions.UnauthorizedError
        return username

    def __verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        """Проверяет правильность введенного пароля сравнением с хешированным.

        Аргументы:
            plain_password: str - введенный пароль
            hashed_password: str - хешированный пароль
        """
        return PASSWORD_CONTEXT.verify(plain_password, hashed_password)

    async def __authenticate_user(
        self, auth_data: UserAuthenticateRequest
    ) -> UserResponse:
        """Аутентифицирует пользователя по `username` и `password` полям.

        Аргументы:
            auth_data: UserAuthenticateRequest - схема для аутентификации
        """
        user = await self.__crud.get_by_username(username=auth_data.username)
        if user.is_blocked:
            raise custom_exceptions.UserBlockedError
        password = auth_data.password.get_secret_value()
        if not self.__verify_password(password, user.password):
            return custom_exceptions.InvalidAuthenticationDataError
        return user

    def __create_token(
        self, username: str, expires_delta: timedelta | None = None
    ) -> str:
        """Создает access-токен.

        Аргументы:
            username: str - никнейм/логин пользователя
            expires_delta: int - время жизни токена
        """
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode = {'username': username, 'exp': expire}
        return jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
        )

    async def login_user(
        self, auth_data: UserAuthenticateRequest
    ) -> UserAndTokenDTO:
        """Аутентифицирует пользователя по `username` и `password` полям.

        Возвращает информацию об администраторе и `access`- токен.

        Аргументы:
            auth_data: UserAuthenticateRequest - схема для аутентификации
        """
        user = await self.__authenticate_user(auth_data=auth_data)
        return UserAndTokenDTO(
            access_token=self.__create_token(
                username=auth_data.username,
                expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
            ),
            user=user
        )

    async def get_current_user(
        self, token: HTTPAuthorizationCredentials
    ) -> UserResponse:
        """Возвращает текущего пользователя по токену.

        Аргументы:
            token: HTTPAuthorizationCredentials - схема авторизации
        """
        username = self.get_username_from_token(token=token.credentials)
        user = await self.__crud.get_by_username(username=username)
        if user.is_blocked:
            raise custom_exceptions.UserBlockedError
        return user

    async def check_current_user_exists(
        self,
        token: HTTPAuthorizationCredentials,
        statuses: list[User.Status] | None = None
    ) -> None:
        """Производит авторизацию пользователя по токену.

        Выбрасывает исключение если пользователь не обнаружен.
        Если определен аргумент `statuses` - пользователь дополнительно
        проверяется на наличие статуса из списка.

        Аргументы:
            token: HTTPAuthorizationCredentials - схема авторизации
            statuses: list[User.Status] - список статусов пользователя
        """
        username = self.get_username_from_token(token=token.credentials)
        if statuses:
            for status in statuses:
                if status not in User.Status.__members__.values():
                    raise custom_exceptions.UserUnknownStatusError(status)
        user_exists = await self.__crud.is_user_exists(username, statuses)
        if not user_exists:
            raise custom_exceptions.ForbiddenError
