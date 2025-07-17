"""
Базовый CRUD-класс для асинхронной работы с моделями SQLAlchemy.

Содержит универсальные методы для получения, создания, обновления и удаления объектов.
"""

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models import User

class CRUDBase:
    """
    Базовый класс для CRUD-операций с моделями SQLAlchemy.
    """
    def __init__(self, model):
        """
        Инициализация CRUDBase.

        Args:
            model: Класс модели SQLAlchemy.
        """
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """
        Получить объект по ID.

        Args:
            obj_id (int): ID объекта.
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            Объект модели или None.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        """
        Получить все объекты модели.

        Args:
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            Список объектов модели.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        """
        Создать новый объект модели.

        Args:
            obj_in: Pydantic-схема с данными для создания.
            session (AsyncSession): Асинхронная сессия БД.
            user (Optional[User]): Пользователь (если требуется связь).

        Returns:
            Созданный объект модели.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """
        Обновить существующий объект модели.

        Args:
            db_obj: Объект модели для обновления.
            obj_in: Pydantic-схема с обновлёнными данными.
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            Обновлённый объект модели.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """
        Удалить объект модели.

        Args:
            db_obj: Объект модели для удаления.
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            Удалённый объект модели.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ):
        """
        Получить объект по значению произвольного атрибута.

        Args:
            attr_name (str): Имя атрибута.
            attr_value (str): Значение атрибута.
            session (AsyncSession): Асинхронная сессия БД.

        Returns:
            Объект модели или None.
        """
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()
