"""
CRUD-операции для модели MeetingRoom (переговорные комнаты).

Содержит методы для поиска комнаты по имени.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom

class CRUDMeetingRoom(CRUDBase):
    """
    CRUD-класс для работы с переговорными комнатами.
    """
    async def get_room_id_by_name(
        self,
        room_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """
        Получить ID переговорной комнаты по имени.

        Args:
            room_name (str): Имя комнаты.
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            Optional[int]: ID комнаты или None, если не найдена.
        """
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
                MeetingRoom.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
