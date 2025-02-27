import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from middlewares.Token_valid import get_current_user_id
from cache.redis.redis_requests import get_event_history_cache, set_event_history_cache
from schemas.history_events_schemas import EventHistoryResponse, HistoryDateFrom, HistoryDateTo
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_event_history_by_dates, get_player
from schemas.error_schemas import InternalServerErrorResponse
from fastapi.security import HTTPBearer
router = APIRouter()
security = HTTPBearer()

@router.post("/events/history", response_model=list[EventHistoryResponse],dependencies=[Depends(security)])
async def get_event_history_route(
    dtfrom: HistoryDateFrom,
    dtto: HistoryDateTo,
    user_id:int=Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить историю событий (history) для игрока за указанный диапазон дат.
    """
    try:
        # Расшифровка токена для получения ID текущего пользователя
        event_history_cache = await  get_event_history_cache(user_id, dtfrom.dtfrom.date(), dtto.dtto.date())
        if event_history_cache:
            return json.loads(event_history_cache)

        player = await get_player(user_id, db)

        # Получение истории событий
        event_history = await get_event_history_by_dates(player.id, dtfrom.dtfrom, dtto.dtto, db)

        await set_event_history_cache(user_id, dtfrom.dtfrom.date(), dtto.dtto.date(), event_history)

        # Формируем ответ
        response = [
            EventHistoryResponse(
                event_name=event.event.name,  # Получаем название события
                description=event.event.description,  # Получаем описание события
                state=event.state,
            )
            for event in event_history
        ]
        return response


    except Exception as e:

        raise HTTPException(status_code=InternalServerErrorResponse.status,

                            detail=InternalServerErrorResponse.status_text)
