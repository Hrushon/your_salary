from pydantic import Field, PastDate, SecretStr, StrictStr

from api.v1.response_models.department import Department
from api.v1.response_models.position import Position
from api.v1.response_models.salary import Salary

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
    password: SecretStr
    date_of_birth: PastDate
    department: Department.id | None
    position: Position.id | None
    salary: Salary.id | None

    _validate_first_name = first_and_last_name_validator('first_name')
    _validate_last_name = first_and_last_name_validator('last_name')
    _validate_pusername = username_validator('username')


class UserAuthenticateRequest(BaseRequest):
    username: StrictStr = Field(min_length=2, max_length=150)
    password: SecretStr
