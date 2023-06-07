from dataclasses import dataclass

from src.data_base.models import User


@dataclass
class UserAndTokenDTO:
    user: User
    access_token: str
