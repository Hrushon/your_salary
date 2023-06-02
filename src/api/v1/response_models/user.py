from datetime import date

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    date_of_birth: date
    is_blocked: bool
    status: str
    department: str | None
    position: str | None

    class Config:
        orm_mode = True


class UserInDB(UserResponse):
    password: str

    class Config:
        orm_mode = True
