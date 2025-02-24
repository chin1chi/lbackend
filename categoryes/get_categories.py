import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cache.redis.redis_requests import get_categories_cache, set_categories_cache
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_player, get_all_categories, update_player_entertainment_tags
from schemas.categories import EntertainmentRequest, LikeRequest, PlayerCategoriesResponse
from schemas.error_schemas import InternalServerErrorResponse, SuccessResponse
from middlewares.Token_valid import get_current_user_id

router = APIRouter()


@router.post("/get_categories_and_player_likes", response_model=PlayerCategoriesResponse)
async def get_categories_and_player_likes(user_id:int=Depends(get_current_user_id), db: AsyncSession = Depends(get_async_session)):
    try:
        categories_cache = await get_categories_cache(user_id)
        if categories_cache:
            return PlayerCategoriesResponse(data=json.loads(categories_cache))

        player = await get_player(user_id, db)

        player_entertainment_tags = player.entertainments_tags

        all_categories = await get_all_categories(db)

        categories_mapping = {
            category.entertainment: (category.id in player_entertainment_tags) for category in all_categories
        }

        await set_categories_cache(user_id, categories_mapping)

        return PlayerCategoriesResponse(data=categories_mapping)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/save_like_category", response_model=SuccessResponse)
async def player_save_like_category(category_request: EntertainmentRequest,
                                    like_request: LikeRequest,user_id:int=Depends(get_current_user_id) ,db: AsyncSession = Depends(get_async_session)):
    try:
        player = await get_player(user_id, db)

        await update_player_entertainment_tags(player, category_request.category_id, like_request.like, db)

        return {SuccessResponse.status: SuccessResponse.status_text}

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)
