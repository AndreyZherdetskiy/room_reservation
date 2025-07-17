"""
Эндпоинты для управления переговорными комнатами.

Содержит CRUD-операции для переговорных комнат и получение бронирований по комнате.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
from app.schemas.reservation import ReservationDB
from app.api.endpoints.constants import MeetingRoomConstants

router = APIRouter()


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=MeetingRoomConstants.CREATE_SUMMARY,
    description=MeetingRoomConstants.CREATE_DESCRIPTION,
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoomDB:
    """
    Создать новую переговорную комнату (только для суперпользователей).
    
    Args:
        meeting_room (MeetingRoomCreate): Данные для создания комнаты.
        session (AsyncSession): Асинхронная сессия БД.
    
    Returns:
        MeetingRoomDB: Созданная комната.
    """
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
    summary=MeetingRoomConstants.GET_ALL_SUMMARY,
    description=MeetingRoomConstants.GET_ALL_DESCRIPTION,
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
) -> list[MeetingRoomDB]:
    """
    Получить список всех переговорных комнат.
    
    Args:
        session (AsyncSession): Асинхронная сессия БД.
    
    Returns:
        list[MeetingRoomDB]: Список комнат.
    """
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=MeetingRoomConstants.UPDATE_SUMMARY,
    description=MeetingRoomConstants.UPDATE_DESCRIPTION,
)
async def partially_update_meeting_room(
    meeting_room_id: int,
    obj_in: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoomDB:
    """
    Частично обновить переговорную комнату (только для суперпользователей).
    
    Args:
        meeting_room_id (int): ID комнаты.
        obj_in (MeetingRoomUpdate): Данные для обновления.
        session (AsyncSession): Асинхронная сессия БД.
    
    Returns:
        MeetingRoomDB: Обновлённая комната.
    """
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=MeetingRoomConstants.DELETE_SUMMARY,
    description=MeetingRoomConstants.DELETE_DESCRIPTION,
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> MeetingRoomDB:
    """
    Удалить переговорную комнату (только для суперпользователей).
    
    Args:
        meeting_room_id (int): ID комнаты.
        session (AsyncSession): Асинхронная сессия БД.
    
    Returns:
        MeetingRoomDB: Удалённая комната.
    """
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
    summary=MeetingRoomConstants.GET_RESERVATIONS_SUMMARY,
    description=MeetingRoomConstants.GET_RESERVATIONS_DESCRIPTION,
)
async def get_reservations_for_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[ReservationDB]:
    """
    Получить список будущих бронирований для выбранной переговорной комнаты.
    
    Args:
        meeting_room_id (int): ID комнаты.
        session (AsyncSession): Асинхронная сессия БД.
    
    Returns:
        list[ReservationDB]: Список бронирований.
    """
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservations
