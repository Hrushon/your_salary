from datetime import date

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    date_of_birth: date
    is_blocked: bool
    status: str
    department: str
    position: str


class UserInDB(User):
    password: str
