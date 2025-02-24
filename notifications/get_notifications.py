import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from cache.redis.redis_requests import get_notifications_cache, set_notifications_cache
from database.connection_to_db.database import get_async_session
from database.request_to_db.database_requests import get_notifications, set_checked_notification_for_user
from schemas.error_schemas import InternalServerErrorResponse, SuccessResponse
from schemas.notifications_schemas import IsCheckedNotificationRequest, NotificationResponse, NotificationInfo, \
    NotificationRequest
from schemas.token_schemas import TokenRequest
from utils.auth_utils import decode_jwt_token

router = APIRouter()


@router.post("/get_notifications")
async def get_notifications_for_user(token: TokenRequest, is_checked: IsCheckedNotificationRequest,
                                     db: AsyncSession = Depends(get_async_session)):
    try:
        current_user_id = decode_jwt_token(token.token)

        notifications_cache = await get_notifications_cache(current_user_id, is_checked.is_checked)
        if notifications_cache:
            return NotificationResponse(data=json.loads(notifications_cache))

        notifications = await get_notifications(current_user_id, is_checked.is_checked, db)

        data = [NotificationInfo(id=notification.id, message=notification.message) for notification in notifications]

        await set_notifications_cache(current_user_id, is_checked.is_checked, data)

        return NotificationResponse(data=data)

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)


@router.post("/set_checked")
async def set_checked_notification(token: TokenRequest, notification: NotificationRequest,
                                   db: AsyncSession = Depends(get_async_session)):
    try:
        current_user_id = decode_jwt_token(token.token)

        await set_checked_notification_for_user(current_user_id, notification.notification_id, db)

        return SuccessResponse()

    except Exception as e:
        raise HTTPException(status_code=InternalServerErrorResponse.status,
                            detail=InternalServerErrorResponse.status_text)
