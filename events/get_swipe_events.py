import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cache.redis.redis_requests import get_random_events_cache, set_random_events_cache, get_swipe_events_cache, \
    set_swipe_events_cache
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_number_random_events, get_swipe_events, add_swipe_event, \
    update_swipe_event, get_swipe_event
from middlewares.Token_valid import get_current_user_id
from schemas.error_schemas import InternalServerErrorResponse, SuccessResponse
from schemas.events_schemas import CountEventsRequest, EventResponse, EventInfo, EventIdRequest
from schemas.swipe_events_schemas import LikeSwipeEventRequest, IsLikeSwipeEventsRequest
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/get_events",dependencies=[Depends(security)])
async def get_events_for_player(
        count_events: CountEventsRequest,
        user_id = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_async_session)):
    try:

        random_events_cache = await get_random_events_cache(user_id, count_events.count_events)
        if random_events_cache:
            return EventResponse(data=json.loads(random_events_cache))

        events = await get_number_random_events(user_id, count_events.count_events, db)

        data = [EventInfo(id=event.id, name=event.name, description=event.description, media=event.media) for event in
                events]

        await set_random_events_cache(user_id, count_events.count_events, data)

        return EventResponse(data=data)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/get_swipe_events",dependencies=[Depends(security)])
async def get_swipe_events_for_player( is_like_swipe_events: IsLikeSwipeEventsRequest,
                                       user_id = Depends(get_current_user_id),
                                      db: AsyncSession = Depends(get_async_session)):
    try:

        swipe_events_cache = await get_swipe_events_cache(user_id, is_like_swipe_events.is_like_events)
        if swipe_events_cache:
            return EventResponse(data=json.loads(swipe_events_cache))

        events = await get_swipe_events(user_id, is_like_swipe_events.is_like_events, db)

        data = [EventInfo(id=event.id, name=event.name, description=event.description, media=event.media) for event in
                events]

        await set_swipe_events_cache(user_id, is_like_swipe_events.is_like_events, data)

        return EventResponse(data=data)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/swipe_event", response_model=SuccessResponse,dependencies=[Depends(security)])
async def player_swipe_event_add_or_update(event_id_request: EventIdRequest,
                                           is_like_event_request: LikeSwipeEventRequest,
                                           user_id = Depends(get_current_user_id),
                                           db: AsyncSession = Depends(get_async_session)):
    try:
        swipe_event = await get_swipe_event(user_id, event_id_request.event_id, db)
        if swipe_event:
            await update_swipe_event(swipe_event, is_like_event_request.is_like_event, db)
        else:
            await add_swipe_event(user_id, event_id_request.event_id, is_like_event_request.is_like_event, db)

        return SuccessResponse()

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)
