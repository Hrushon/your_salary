from pydantic import Field, PastDate, PositiveInt, SecretStr, StrictStr

from .base_request import BaseRequest
from .validators import first_and_last_name_validator, username_validator


class Token(BaseRequest):
    access_token: StrictStr
    token_type: StrictStr


class TokenData(BaseRequest):
    username: str | None = None


class UserCreateRequest(BaseRequest):
    first_name: StrictStr = Field(min_length=2, max_length=150)
    last_name: StrictStr = Field(min_length=2, max_length=150)
    username: StrictStr = Field(min_length=2, max_length=150)
    password: StrictStr
    date_of_birth: PastDate
    department: PositiveInt | None
    position: PositiveInt | None
    salary: PositiveInt | None

    _validate_first_name = first_and_last_name_validator('first_name')
    _validate_last_name = first_and_last_name_validator('last_name')
    _validate_pusername = username_validator('username')


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
    password: SecretStr
