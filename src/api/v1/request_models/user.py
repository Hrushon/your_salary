from pydantic import Field, PastDate, PositiveInt, SecretStr, StrictStr

from src.data_base.models import User

from .base_request import BaseRequest
from .validators import (first_and_last_name_validator, password_validator,
                         username_validator)


class TokenData(BaseRequest):
    username: str | None = None


class UserCreateRequest(BaseRequest):
    first_name: StrictStr = Field(min_length=2, max_length=150)
    last_name: StrictStr = Field(min_length=2, max_length=150)
    username: StrictStr = Field(min_length=2, max_length=150)
    password: SecretStr = Field(min_length=8)
    password_repeat: SecretStr = Field(min_length=8)
    date_of_birth: PastDate

    _validate_first_name = first_and_last_name_validator('first_name')
    _validate_last_name = first_and_last_name_validator('last_name')
    _validate_username = username_validator('username')
    _validate_password = password_validator('password_repeat')


class UserSelfUpdateRequest(BaseRequest):
    first_name: StrictStr | None = Field(min_length=2, max_length=150)
    last_name: StrictStr | None = Field(min_length=2, max_length=150)
    date_of_birth: PastDate | None

    _validate_first_name = first_and_last_name_validator('first_name')
    _validate_last_name = first_and_last_name_validator('last_name')


class UserResetPasswordRequest(BaseRequest):
    password: SecretStr = Field(min_length=8)
    password_repeat: SecretStr = Field(min_length=8)

    _validate_password = password_validator('password_repeat')


class UserUpdateRequest(BaseRequest):
    first_name: StrictStr | None = Field(min_length=2, max_length=150)
    last_name: StrictStr | None = Field(min_length=2, max_length=150)
    date_of_birth: PastDate | None
    department: PositiveInt | None
    position: PositiveInt | None
    salary: PositiveInt | None

    _validate_first_name = first_and_last_name_validator('first_name')
    _validate_last_name = first_and_last_name_validator('last_name')


class UserAuthenticateRequest(BaseRequest):
    username: StrictStr = Field(min_length=2, max_length=150)
    password: SecretStr = Field(min_length=8)


class UserChangeStatusRequest(BaseRequest):
    status: User.Status
