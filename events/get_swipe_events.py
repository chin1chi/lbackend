import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cache.redis.redis_requests import get_random_events_cache, set_random_events_cache, get_swipe_events_cache, \
    set_swipe_events_cache
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_number_random_events, get_swipe_events, add_swipe_event, \
    update_swipe_event, get_swipe_event
from schemas.error_schemas import InternalServerErrorResponse, SuccessResponse
from schemas.events_schemas import CountEventsRequest, EventResponse, EventInfo, EventIdRequest
from schemas.swipe_events_schemas import LikeSwipeEventRequest, IsLikeSwipeEventsRequest
from schemas.token_schemas import TokenRequest
from utils.auth_utils import decode_jwt_token

router = APIRouter()


@router.post("/get_events")
async def get_events_for_player(token: TokenRequest, count_events: CountEventsRequest,
                                db: AsyncSession = Depends(get_async_session)):
    try:
        current_user_id = decode_jwt_token(token.token)

        random_events_cache = await get_random_events_cache(current_user_id, count_events.count_events)
        if random_events_cache:
            return EventResponse(data=json.loads(random_events_cache))

        events = await get_number_random_events(current_user_id, count_events.count_events, db)

        data = [EventInfo(id=event.id, name=event.name, description=event.description, media=event.media) for event in
                events]

        await set_random_events_cache(current_user_id, count_events.count_events, data)

        return EventResponse(data=data)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/get_swipe_events")
async def get_swipe_events_for_player(token: TokenRequest, is_like_swipe_events: IsLikeSwipeEventsRequest,
                                      db: AsyncSession = Depends(get_async_session)):
    try:
        current_user_id = decode_jwt_token(token.token)

        swipe_events_cache = await get_swipe_events_cache(current_user_id, is_like_swipe_events.is_like_events)
        if swipe_events_cache:
            return EventResponse(data=json.loads(swipe_events_cache))

        events = await get_swipe_events(current_user_id, is_like_swipe_events.is_like_events, db)

        data = [EventInfo(id=event.id, name=event.name, description=event.description, media=event.media) for event in
                events]

        await set_swipe_events_cache(current_user_id, is_like_swipe_events.is_like_events, data)

        return EventResponse(data=data)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/swipe_event", response_model=SuccessResponse)
async def player_swipe_event_add_or_update(token: TokenRequest, event_id_request: EventIdRequest,
                                           is_like_event_request: LikeSwipeEventRequest,
                                           db: AsyncSession = Depends(get_async_session)):
    try:
        current_user_id = decode_jwt_token(token.token)

        swipe_event = await get_swipe_event(current_user_id, event_id_request.event_id, db)
        if swipe_event:
            await update_swipe_event(swipe_event, is_like_event_request.is_like_event, db)
        else:
            await add_swipe_event(current_user_id, event_id_request.event_id, is_like_event_request.is_like_event, db)

        return SuccessResponse()

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)
