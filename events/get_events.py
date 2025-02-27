# events.py
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from cache.redis.redis_requests import get_ongoing_events_cache, set_ongoing_events_cache, get_details_event_cache, \
    set_details_event_cache
from schemas import events_schemas
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_ongoing_events, get_event_by_id, get_player
from schemas.events_schemas import EventShortInfo
from schemas.error_schemas import InternalServerErrorResponse, SuccessResponse
from  middlewares.Token_valid import get_current_user_id
from schemas.error_schemas import InternalServerErrorResponse
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

@router.post("/events/ongoing", response_model=list[events_schemas.EventShortInfo],
             dependencies=[Depends(security)])

async def get_ongoing_events_route(
    user_id = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить текущие события (ongoing) для игрока.
    """
    try:
        # Расшифровка токена для получения ID текущего пользователя
        ongoing_events_cache = await get_ongoing_events_cache(user_id)
        if ongoing_events_cache:
            return json.loads(ongoing_events_cache)
        # Получаем игрока по ID пользователя
        player = await get_player(user_id, db)

        # Получаем текущие события (ongoing) для данного игрока
        ongoing_events = await get_ongoing_events(player.id, db)

        data = [
            EventShortInfo(
                **{key: value for key, value in event.__dict__.items() if not key.startswith("_")})
            for event in ongoing_events
        ]

        await set_ongoing_events_cache(user_id, data)

        # Возвращаем результат
        return data


    except Exception as e:

        logger.error(f"Error in get_ongoing_events_route: {e}", exc_info=True)

        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/events/details", response_model=events_schemas.EventDetailsResponce,
             dependencies=[Depends(security)])
async def get_event_details_by_post(event_request: events_schemas.EventRequest,
                                    user_id = Depends(get_current_user_id),
                                    db: AsyncSession = Depends(get_async_session)):
    """
    Получаем полную информацию по событию по его id, переданному в теле запроса.
    """
    try:


        event_id = event_request.event_id

        details_event_cache = await get_details_event_cache(event_id)
        if details_event_cache:
            return json.loads(details_event_cache)

        event = await get_event_by_id(db, event_id)

        await set_details_event_cache(event_id, event)

        # Возвращаем подробную информацию о событии
        return events_schemas.EventDetailsResponce(
            name=event.name,
            description=event.description,
            location=event.location,
            started_at=event.started_at,
            expired_at=event.expired_at,
            price=event.price,
            media=event.media,
            inst=event.inst,
        )

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)
