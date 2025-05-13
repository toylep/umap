from abc import ABC, abstractmethod

from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from config.db import AsyncSessionLocal
from sqlalchemy.sql import and_
from sqlalchemy.orm import joinedload


class AbstractRepo(ABC):

    @abstractmethod
    async def get_all(self):
        """
        Получение всех моделей
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_with_filters(self, return_single=False, **filter_by):
        """
        Получение конкретной модели
        """
        raise NotImplementedError()

    @abstractmethod
    async def add(self, model_obj):
        """
        Добавление модели
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, update_data: dict[str, any]):
        """
        Изменение в модели
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int):
        """
        Изменение в модели
        """
        raise NotImplementedError()


class SQLRepo(AbstractRepo):

    model_cls = None

    async def get_all(self, joined_fields: list[any] = []):
        """
        Получение всех моделей
        """
        async with AsyncSessionLocal() as s:
            stmt = select(self.model_cls).options(
                *[joinedload(field) for field in joined_fields]
            )
            result = await s.execute(stmt)
        return result.scalars().unique().all()

    async def get_with_filters(
        self,
        filter_by: dict[str, any],
        return_single=False,
        joined_fields: list[any] = [],
        # sort_by: list[any] = [],
    ):
        """
        Получение обьектов или обьекта по фильтрам
        """
        filter_conditions = []
        for field, value in filter_by.items():
            # Проверяем, есть ли поле в модели
            if hasattr(self.model_cls, field):
                column = getattr(self.model_cls, field)
                if isinstance(value, (list, tuple)):  # Если передан диапазон
                    filter_conditions.append(column.in_(value))
                elif value == "not_none":  # Условие IS NOT NULL
                    filter_conditions.append(column.isnot(None))
                elif value == "none":  # Условие IS NULL
                    filter_conditions.append(column.is_(None))
                else:
                    filter_conditions.append(column == value)

        async with AsyncSessionLocal() as s:
            stmt = (
                select(self.model_cls)
                .where(and_(*filter_conditions))
                .options(*[joinedload(field) for field in joined_fields])
            )
            result = await s.execute(stmt)
            return (
                result.scalars().unique().all()
                if not return_single
                else result.scalars().first()
            )

    async def update(self, id: int, update_data: dict[str, any]):
        """
        Изменение модели
        """
        async with AsyncSessionLocal() as s:
            stmt = (
                update(self.model_cls)
                .where(self.model_cls.id == id)
                .values(**update_data)
                .returning(self.model_cls)
            )
            result = await s.execute(stmt)
            await s.commit()
        return result.scalar_one()
    
    async def delete(self, id):
        """
        Удаление модели
        """
        async with AsyncSessionLocal() as s:
            stmt = delete(self.model_cls.id).where(self.model_cls.id == id)
            result = await s.execute(stmt)
            await s.commit()
        return result.scalars().first()

    async def add(self, data: dict[str, any]):
        """
        Добавление модели
        """
        async with AsyncSessionLocal() as s:
            stmt = (
                insert(self.model_cls)
                .values(**data)
                .returning(self.model_cls)  # Указываем, что хотим вернуть
            )
            result = await s.execute(stmt)
            await s.commit()
        return result.scalar_one()
