"""
Модуль конфигурации приложения. Использует Pydantic для управления настройками.
"""

from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    Класс конфигурации приложения. Все параметры берутся из переменных окружения или .env.
    """
    app_title: str = 'Бронирование переговорок'
    database_url: str
    description: str = 'Описание проекта'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
