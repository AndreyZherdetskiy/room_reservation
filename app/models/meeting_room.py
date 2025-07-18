"""
SQLAlchemy-модель переговорной комнаты.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.constants import MeetingRoomModelConstants

class MeetingRoom(Base):
    """
    Модель переговорной комнаты.

    Атрибуты:
        name (str): Название комнаты.
        description (str): Описание комнаты.
        reservations: Связанные бронирования.
    """
    name = Column(String(MeetingRoomModelConstants.MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text)
    reservations = relationship('Reservation', cascade='delete')
