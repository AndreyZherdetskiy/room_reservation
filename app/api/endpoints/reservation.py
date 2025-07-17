"""
Эндпоинты для управления бронированиями переговорных комнат.

Содержит CRUD-операции для бронирований и получение бронирований пользователя.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.reservation import reservation_crud
from app.models import User
from app.schemas.reservation import ReservationCreate, ReservationDB, ReservationUpdate
from app.api.endpoints.constants import ReservationConstants

router = APIRouter()


@router.post(
    '/',
    response_model=ReservationDB,
    summary=ReservationConstants.CREATE_SUMMARY,
    description=ReservationConstants.CREATE_DESCRIPTION,
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> ReservationDB:
    """
    Создать новое бронирование переговорной комнаты.

    Args:
        reservation (ReservationCreate): Данные для создания бронирования.
        session (AsyncSession): Асинхронная сессия БД.
        user (User): Текущий пользователь.

    Returns:
        ReservationDB: Созданное бронирование.
    """
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(**reservation.dict(), session=session)
    new_reservation = await reservation_crud.create(reservation, session, user)
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB],
    dependencies=[Depends(current_superuser)],
    summary=ReservationConstants.GET_ALL_SUMMARY,
    description=ReservationConstants.GET_ALL_DESCRIPTION,
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
) -> list[ReservationDB]:
    """
    Получить список всех бронирований (только для суперпользователей).

    Args:
        session (AsyncSession): Асинхронная сессия БД.

    Returns:
        list[ReservationDB]: Список бронирований.
    """
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB,
    summary=ReservationConstants.DELETE_SUMMARY,
    description=ReservationConstants.DELETE_DESCRIPTION,
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> ReservationDB:
    """
    Удалить бронирование (только владелец или суперпользователь).

    Args:
        reservation_id (int): ID бронирования.
        session (AsyncSession): Асинхронная сессия БД.
        user (User): Текущий пользователь.

    Returns:
        ReservationDB: Удалённое бронирование.
    """
    reservation = await check_reservation_before_edit(reservation_id, session, user)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch(
    '/{reservation_id}',
    response_model=ReservationDB,
    summary=ReservationConstants.UPDATE_SUMMARY,
    description=ReservationConstants.UPDATE_DESCRIPTION,
)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> ReservationDB:
    """
    Обновить бронирование (только владелец или суперпользователь).

    Args:
        reservation_id (int): ID бронирования.
        obj_in (ReservationUpdate): Данные для обновления.
        session (AsyncSession): Асинхронная сессия БД.
        user (User): Текущий пользователь.

    Returns:
        ReservationDB: Обновлённое бронирование.
    """
    reservation = await check_reservation_before_edit(reservation_id, session, user)
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=obj_in,
        session=session,
    )
    return reservation


@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    response_model_exclude={'user_id'},
    summary=ReservationConstants.GET_MY_SUMMARY,
    description=ReservationConstants.GET_MY_DESCRIPTION,
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> list[ReservationDB]:
    """
    Получить список всех бронирований для текущего пользователя.

    Args:
        session (AsyncSession): Асинхронная сессия БД.
        user (User): Текущий пользователь.

    Returns:
        list[ReservationDB]: Список бронирований пользователя.
    """
    reservations = await reservation_crud.get_by_user(session=session, user=user)
    return reservations
