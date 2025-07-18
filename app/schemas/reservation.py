"""
Pydantic-схемы для работы с бронированиями переговорных комнат.
"""

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, root_validator, validator
from app.schemas.constants import ReservationMessages, ReservationTimeDefaults

FROM_TIME = (
    datetime.now() + timedelta(minutes=ReservationTimeDefaults.FROM_MINUTES_SHIFT)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=ReservationTimeDefaults.TO_HOURS_SHIFT)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    """
    Базовая схема бронирования.

    Attributes:
        from_reserve (datetime): Время начала бронирования.
        to_reserve (datetime): Время окончания бронирования.
    """
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):
    """
    Схема обновления бронирования с валидацией дат.
    """
    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: datetime) -> datetime:
        """
        Проверяет, что время начала бронирования больше текущего времени.

        Args:
            value (datetime): Время начала бронирования.

        Returns:
            datetime: Проверенное значение.

        Raises:
            ValueError: Если время начала меньше текущего.
        """
        if value <= datetime.now():
            raise ValueError(
                ReservationMessages.FROM_LESS_THAN_NOW
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values: dict) -> dict:
        """
        Проверяет, что время начала бронирования меньше времени окончания.

        Args:
            values (dict): Значения полей.

        Returns:
            dict: Проверенные значения.

        Raises:
            ValueError: Если from_reserve >= to_reserve.
        """
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                ReservationMessages.FROM_MORE_THAN_TO
            )
        return values


class ReservationCreate(ReservationUpdate):
    """
    Схема создания бронирования.

    Attributes:
        meetingroom_id (int): ID переговорной комнаты.
    """
    meetingroom_id: int


class ReservationDB(ReservationBase):
    """
    Схема для возврата бронирования из БД.

    Attributes:
        id (int): ID бронирования.
        meetingroom_id (int): ID переговорной комнаты.
        user_id (Optional[int]): ID пользователя.
    """
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True
