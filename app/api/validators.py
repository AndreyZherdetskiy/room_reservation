"""
Валидаторы бизнес-логики для бронирования и переговорных комнат.

Содержит проверки уникальности имени, существования объектов и прав пользователя.
"""

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import MeetingRoom, Reservation, User
from app.api.constants import MeetingRoomDetail, ReservationDetail


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession,
) -> None:
    """
    Проверяет уникальность имени переговорной комнаты.

    Args:
        room_name (str): Имя комнаты.
        session (AsyncSession): Асинхронная сессия БД.

    Raises:
        HTTPException: Если комната с таким именем уже существует.
    """
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=MeetingRoomDetail.DUPLICATE_NAME,
        )


async def check_meeting_room_exists(
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    """
    Проверяет существование переговорной комнаты по ID.

    Args:
        meeting_room_id (int): ID комнаты.
        session (AsyncSession): Асинхронная сессия БД.

    Returns:
        MeetingRoom: Объект комнаты.

    Raises:
        HTTPException: Если комната не найдена.
    """
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=MeetingRoomDetail.NOT_FOUND
        )
    return meeting_room


async def check_reservation_intersections(**kwargs) -> None:
    """
    Проверяет пересечения бронирований по времени и комнате.

    Args:
        **kwargs: Параметры фильтрации бронирований.

    Raises:
        HTTPException: Если есть пересекающиеся бронирования.
    """
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ReservationDetail.INTERSECTION
        )


async def check_reservation_before_edit(
    reservation_id: int,
    session: AsyncSession,
    user: User
) -> Reservation:
    """
    Проверяет права пользователя и существование бронирования перед изменением/удалением.

    Args:
        reservation_id (int): ID бронирования.
        session (AsyncSession): Асинхронная сессия БД.
        user (User): Текущий пользователь.

    Returns:
        Reservation: Объект бронирования.

    Raises:
        HTTPException: Если бронь не найдена или нет прав на изменение.
    """
    reservation = await reservation_crud.get(
        obj_id=reservation_id, session=session
    )
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ReservationDetail.NOT_FOUND)
    if reservation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ReservationDetail.FORBIDDEN
        )
    return reservation
