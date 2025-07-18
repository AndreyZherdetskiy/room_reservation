"""
Pydantic-схемы для работы с переговорными комнатами.
"""

from typing import Optional

from pydantic import BaseModel, Field, validator
from app.schemas.constants import SchemaBaseConstants, MeetingRoomMessages

class MeetingRoomBase(BaseModel):
    """
    Базовая схема переговорной комнаты.

    Attributes:
        name (Optional[str]): Название комнаты.
        description (Optional[str]): Описание комнаты.
    """
    name: Optional[str] = Field(None, min_length=SchemaBaseConstants.MIN_NAME_LENGTH, max_length=SchemaBaseConstants.MAX_NAME_LENGTH)
    description: Optional[str]

class MeetingRoomCreate(MeetingRoomBase):
    """
    Схема для создания переговорной комнаты.

    Attributes:
        name (str): Название комнаты (обязательное).
    """
    name: str = Field(..., min_length=SchemaBaseConstants.MIN_NAME_LENGTH, max_length=SchemaBaseConstants.MAX_NAME_LENGTH)

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
            raise ValueError(MeetingRoomMessages.EMPTY_NAME)
        if len(value) > SchemaBaseConstants.MAX_NAME_LENGTH:
            raise ValueError(MeetingRoomMessages.NAME_TOO_LONG)
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
            raise ValueError(MeetingRoomMessages.EMPTY_NAME_UPDATE)
        if len(value) > SchemaBaseConstants.MAX_NAME_LENGTH:
            raise ValueError(MeetingRoomMessages.NAME_TOO_LONG)
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
