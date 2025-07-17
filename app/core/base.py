"""
Модуль для Alembic: импортирует Base и все модели.
"""

from app.core.db import Base  # noqa
from app.models import MeetingRoom, Reservation, User  # noqa
