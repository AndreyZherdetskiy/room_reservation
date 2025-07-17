"""
CRUD-операции для модели Reservation (бронирование переговорных комнат).

Содержит методы для поиска пересечений, получения будущих бронирований и бронирований пользователя.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.models.user import User

class CRUDReservation(CRUDBase):
    """
    CRUD-класс для работы с бронированиями переговорных комнат.
    """
    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        """
        Получить список бронирований, пересекающихся по времени и комнате.

        Args:
            from_reserve (datetime): Начало нового бронирования.
            to_reserve (datetime): Конец нового бронирования.
            meetingroom_id (int): ID переговорной комнаты.
            reservation_id (Optional[int]): Исключить бронирование с этим ID (например, при обновлении).
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            list[Reservation]: Список пересекающихся бронирований.
        """
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
        self,
        room_id: int,
        session: AsyncSession,
    ) -> list[Reservation]:
        """
        Получить все будущие бронирования для переговорной комнаты.

        Args:
            room_id (int): ID переговорной комнаты.
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            list[Reservation]: Список будущих бронирований.
        """
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> list[Reservation]:
        """
        Получить все бронирования пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия БД.
            user (User): Пользователь.

        Returns:
            list[Reservation]: Список бронирований пользователя.
        """
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        return reservations.scalars().all()

reservation_crud = CRUDReservation(Reservation)
