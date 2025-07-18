"""
SQLAlchemy-модель пользователя для FastAPI Users.
"""

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя для FastAPI Users.
    """
    pass
