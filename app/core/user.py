"""
Модуль управления пользователями и аутентификацией.
"""

from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.constants import UserPasswordConstants, JWTConstants
from app.models.user import User
from app.schemas.user import UserCreate

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Провайдер базы данных пользователей для FastAPI Users.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Yields:
        SQLAlchemyUserDatabase: Провайдер пользователей.
    """
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Возвращает стратегию JWT для аутентификации пользователей.

    Returns:
        JWTStrategy: Стратегия JWT.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=JWTConstants.LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Менеджер пользователей с кастомной валидацией пароля и хуками событий.
    """
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Проверяет валидность пароля пользователя.

        Args:
            password (str): Пароль.
            user (UserCreate | User): Пользователь.

        Raises:
            InvalidPasswordException: Если пароль невалиден.
        """
        if len(password) < UserPasswordConstants.MIN_LENGTH:
            raise InvalidPasswordException(
                reason=UserPasswordConstants.TOO_SHORT
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=UserPasswordConstants.CONTAINS_EMAIL
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """
        Хук, вызываемый после успешной регистрации пользователя.

        Args:
            user (User): Зарегистрированный пользователь.
            request (Optional[Request]): Запрос FastAPI.
        """
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Провайдер менеджера пользователей для FastAPI Users.

    Args:
        user_db: Провайдер базы пользователей.

    Yields:
        UserManager: Менеджер пользователей.
    """
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
