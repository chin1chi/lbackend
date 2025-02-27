import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cache.redis.redis_requests import get_rating_cache, set_rating_cache
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import players_rating_all, players_rating_current_month, \
    players_rating_current_year, get_username_by_user_id
from schemas.error_schemas import InternalServerErrorResponse
from schemas.rating_schemas import RatingResponse, PlayerRating
from middlewares.Token_valid import get_current_user_id
from fastapi.security import HTTPBearer
router = APIRouter()
security = HTTPBearer()

async def top_100_rating_player(user_id, players, db):
    current_username = await get_username_by_user_id(user_id, db)
    rating_players = []
    found_user = None

    for position, (username, points_value) in enumerate(players):
        if position < 100:
            rating_players.append(PlayerRating(position=position + 1, username=username, points_value=points_value))
        elif found_user:
            break
        if username == current_username:
            found_user = PlayerRating(position=position + 1, username=username, points_value=points_value)

    if found_user and found_user not in rating_players:
        rating_players.append(found_user)
    elif not found_user:
        rating_players.append(PlayerRating(position=len(rating_players) + 1, username=current_username, points_value=0))

    return rating_players


@router.post("/all",dependencies=[Depends(security)])
async def get_all_rating(user_id:int=Depends(get_current_user_id), db: AsyncSession = Depends(get_async_session)):
    try:
        rating_cache = await get_rating_cache(user_id, "all")

        if rating_cache:
            return RatingResponse(data=json.loads(rating_cache))

        players = await players_rating_all(db)
        data = await top_100_rating_player(user_id, players, db)

        await set_rating_cache(user_id, "all", data)

        return RatingResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/current_month",dependencies=[Depends(security)])
async def get_rating_current_month(user_id:int=Depends(get_current_user_id), db: AsyncSession = Depends(get_async_session)):
    try:
        rating_cache = await get_rating_cache(user_id, "current_month")

        if rating_cache:
            return RatingResponse(data=json.loads(rating_cache))
          
        players = await players_rating_current_month(db)
        data = await top_100_rating_player(user_id, players, db)

        await set_rating_cache(user_id, "current_month", data)

        return RatingResponse(data=data)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/current_year",dependencies=[Depends(security)])
async def get_rating_current_year(user_id:int=Depends(get_current_user_id), db: AsyncSession = Depends(get_async_session)):
    try:
        rating_cache = await get_rating_cache(user_id, "current_year")
        if rating_cache:
            return RatingResponse(data=json.loads(rating_cache))

        players = await players_rating_current_year(db)
        data = await top_100_rating_player(user_id, players, db)

        await set_rating_cache(user_id, "current_year", data)

        return RatingResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)
