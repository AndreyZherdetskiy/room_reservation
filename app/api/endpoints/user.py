"""
Эндпоинты для управления пользователями и аутентификацией.

Включает регистрацию, аутентификацию и работу с пользователями через FastAPI Users.
"""

from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.api.endpoints.constants import UserConstants

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
