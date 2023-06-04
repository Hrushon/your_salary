from datetime import date

from pydantic import BaseModel

from src.data_base.models import User


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        orm_mode = True


class TokenDataResponse(BaseModel):
    username: str | None = None

    class Config:
        orm_mode = True


class DepartmentInUserResponse(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class SalaryInUserResponse(BaseModel):
    id: int
    amount: float
    raise_date: date

    class Config:
        orm_mode = True


class PositionInUserResponse(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    date_of_birth: date
    is_blocked: bool
    status: User.Status
    department: DepartmentInUserResponse | None
    position: PositionInUserResponse | None
    salary: SalaryInUserResponse | None

    class Config:
        orm_mode = True


class UserNestedResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    status: User.Status

    class Config:
        orm_mode = True


class UserAndAccessTokenResponse(TokenResponse, UserResponse):

    class Config:
        orm_mode = True
