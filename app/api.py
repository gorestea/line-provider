from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas import EventCreate, EventUpdate, EventResponse
from app.services.event_service import EventService

router = APIRouter()

@router.get("/events", response_model=list[EventResponse])
async def read_events(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список событий с возможностью пагинации.

    - **skip**: Количество пропускаемых записей
    - **limit**: Максимальное количество записей для возврата
    """
    return await EventService.get_events(db, skip, limit)

@router.get("/events/{event_id}", response_model=EventResponse)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    return await EventService.get_event_by_id(event_id, db)

@router.post("/events", response_model=EventResponse)
async def create_event(event: EventCreate = Body(...), db: AsyncSession = Depends(get_db)):
    """
    Создать новое событие.

    - **name**: Название события
    - **odds**: Коэффициент (должен быть положительным числом)
    - **deadline**: Дата и время окончания события (в формате YYYY-MM-DD HH:MM)
    """
    return await EventService.create_event(event, db)

@router.patch("/events/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить статус события.

    - **status**: Новый статус события. Может быть только 3 типа:
    - **незавершённое**
    - **завершено выигрышем первой команды**
    - **завершено выигрышем второй команды**
    """
    event = await EventService.update_event(event_id, event_update, db)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
