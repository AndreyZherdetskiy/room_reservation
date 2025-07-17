"""
Pydantic-схемы для работы с переговорными комнатами.
"""

from typing import Optional

from pydantic import BaseModel, Field, validator

class MeetingRoomBase(BaseModel):
    """
    Базовая схема переговорной комнаты.

    Attributes:
        name (Optional[str]): Название комнаты.
        description (Optional[str]): Описание комнаты.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]

class MeetingRoomCreate(MeetingRoomBase):
    """
    Схема для создания переговорной комнаты.

    Attributes:
        name (str): Название комнаты (обязательное).
    """
    name: str = Field(..., min_length=1, max_length=100)

    @validator('name')
    def validate_name(cls, value: str) -> str:
        """
        Проверяет корректность имени комнаты.

        Args:
            value (str): Имя комнаты.

        Returns:
            str: Проверенное имя.

        Raises:
            ValueError: Если имя пустое или слишком длинное.
        """
        if not value:
            raise ValueError('Строка не должна быть пустой')
        if len(value) > 100:
            raise ValueError('Длина поля не должна превышать 100 символов')
        return value

class MeetingRoomUpdate(MeetingRoomBase):
    """
    Схема для обновления переговорной комнаты.
    """
    @validator('name')
    def validate_name(cls, value: str) -> str:
        """
        Проверяет корректность имени комнаты при обновлении.

        Args:
            value (str): Имя комнаты.

        Returns:
            str: Проверенное имя.

        Raises:
            ValueError: Если имя пустое или слишком длинное.
        """
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        if len(value) > 100:
            raise ValueError('Длина поля не должна превышать 100 символов')
        return value

class MeetingRoomDB(MeetingRoomCreate):
    """
    Схема для возврата переговорной комнаты из БД.

    Attributes:
        id (int): ID комнаты.
    """
    id: int

    class Config:
        orm_mode = True
