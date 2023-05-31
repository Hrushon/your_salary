from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from api.v1.response_models.users import User, TokenData, UserInDB
from src.core import settings

ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
PASSWORD_CONTEXT: CryptContext = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)
OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет правильность введенного пароля сравнением с хешированным."""
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return PASSWORD_CONTEXT.hash(password)


def get_user(db, username: str):

    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str) -> User:
    """Аутентифицирует пользователя по `username` и `password` полям."""
    user = db.get_user(username)
    if not user or user.is_blocked:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создает access-токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
