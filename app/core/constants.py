"""
Константы для ядра приложения (core):
- Ограничения и сообщения для паролей пользователей
- Параметры для JWT-аутентификации
"""

class UserPasswordConstants:
    """
    Константы для валидации паролей пользователей.
    """
    MIN_LENGTH: int = 3
    TOO_SHORT: str = 'Password should be at least 3 characters'
    CONTAINS_EMAIL: str = 'Password should not contain e-mail'

class JWTConstants:
    """
    Константы для настройки JWT-аутентификации.
    """
    LIFETIME_SECONDS: int = 3600 