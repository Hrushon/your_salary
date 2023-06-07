import uuid
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Настройки приложения."""

    # Режим разработки (True/False - Активирован/Деактивирован)
    DEVELOPMENT: bool
    # Режим отладки (True/False - Активирован/Деактивирован)
    DEBUG: bool
    # Секретный ключ для генерации токенов
    SECRET_KEY: str = str(uuid.uuid4())
    # Описание проекта для документации
    DESCRIPTION: str = """
        Приложение `Your Salary ™` позволяет сотруднику просмотреть
        размер текущей заработной платы и даты следующего повышения.
        Сотрудник имеет право смотреть только размер собственной заработной платы.
        Редактировать даты пересмотра и уровень заработной платы других
        сотрудников вправе только сотрудники с отдельным допуском.
    """
    # База данных для режима разработки
    DB_DEV: str = 'sqlite+aiosqlite:///./db.sqlite3'

    # База данных
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    @property
    def get_postgresql_url(self) -> str:
        """Возвращает необходимые данные для подключения `Postgresql`."""
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
