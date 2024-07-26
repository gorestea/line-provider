from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Event
from app.schemas import EventCreate, EventUpdate, EventResponse
from app.rabbit import publish_event_update
from fastapi import HTTPException


class EventService:
    """
    Класс EventService предоставляет методы для работы с событиями.
    """

    @staticmethod
    async def get_events(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[EventResponse]:
        """
        Получение списка событий с возможностью пагинации.

        :param db: Сессия базы данных.
        :param skip: Количество пропускаемых событий.
        :param limit: Максимальное количество возвращаемых событий.
        :return: Список событий.
        """
        result = await db.execute(select(Event).offset(skip).limit(limit))
        events = result.scalars().all()
        return [EventResponse.from_orm(event) for event in events]

    @staticmethod
    async def get_event_by_id(event_id: int, db: AsyncSession) -> EventResponse:
        """
        Получение события по идентификатору.

        :param event_id: Идентификатор события.
        :param db: Сессия базы данных.
        :return: Событие.
        """
        result = await db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return EventResponse.from_orm(event)

    @staticmethod
    async def create_event(event_data: EventCreate, db: AsyncSession) -> EventResponse:
        """
        Создание нового события.

        :param event_data: Данные для создания события.
        :param db: Сессия базы данных.
        :return: Созданное событие.
        """
        # Обрезка datetime до минут
        new_event = Event(
            name=event_data.name,
            odds=event_data.odds,
            deadline=event_data.deadline,
            status="незавершённое"
        )
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return EventResponse.from_orm(new_event)

    @staticmethod
    async def update_event(event_id: int, event_update: EventUpdate, db: AsyncSession) -> EventResponse:
        """
        Обновление статуса события.

        :param event_id: Идентификатор события.
        :param event_update: Данные для обновления статуса события.
        :param db: Сессия базы данных.
        :return: Обновленное событие.
        """
        result = await db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        event.status = event_update.status
        await db.commit()
        await db.refresh(event)
        return EventResponse.from_orm(event)
