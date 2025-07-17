"""
SQLAlchemy-модель для хранения бронирований переговорных комнат.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base

class Reservation(Base):
    """
    Модель бронирования переговорной комнаты.

    Атрибуты:
        from_reserve (datetime): Время начала бронирования.
        to_reserve (datetime): Время окончания бронирования.
        meetingroom_id (int): ID переговорной комнаты.
        user_id (int): ID пользователя.
    """
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_reservation_user_id_user')
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление бронирования.

        Returns:
            str: Строка с датами бронирования.
        """
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
