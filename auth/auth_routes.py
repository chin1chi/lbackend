from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection_to_db.database import get_async_session
from schemas.token_schemas import TokenRequest,RefreshTokenRequest
from schemas.auth_schemas import TokenResponse, CodeVerificationResponse
from utils.auth_utils import create_jwt_token, generate_sms_code, verify_sms_code,create_refresh_token,decode_jwt_token
from cache.redis.redis_requests import store_code
from schemas.auth_schemas import PhoneLoginRequest, CodeVerificationRequest
from database.request_to_db.database_requests import get_user_by_phone, create_user,create_player_for_user
from fastapi.security.api_key import APIKeyHeader
import logging
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login")
async def login_or_create_user(data: PhoneLoginRequest, db: AsyncSession = Depends(get_async_session)):
    # Проверяем, существует ли пользователь
    user = await get_user_by_phone(data.phone, db)
    if user is None:
        # Создаём нового пользователя
        user = await create_user(data.phone, db)

        # Проверяем, связан ли пользователь с партнёрами, и создаём игрока, если нужно
        await create_player_for_user(user, db)

    code = generate_sms_code()
    await store_code(data.phone, code)
    # Тут добавить отправку SMS через внешний сервис
    return CodeVerificationResponse(code=code)


@router.post("/verify-code")
async def verify_code(data: CodeVerificationRequest, db: AsyncSession = Depends(get_async_session)):
    """
    Проверяет введенный код и выдает access_token и refresh_token.
    """
    try:
        is_valid = await verify_sms_code(data.phone, data.code)
        user= await get_user_by_phone(data.phone,db)
        if is_valid:
            # Генерируем токены
            access_token = create_jwt_token(user_id=user.id,)
            refresh_token = create_refresh_token(user_id=user.id,)
            return TokenResponse(access_token=access_token, refresh_token=refresh_token)


        else:
            raise HTTPException(status_code=400, detail="Invalid code")
    except ValueError as e:
        logger.error(f"Error in get_ongoing_events_route: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh-token")
async def refresh_access_token(refresh_token: str):
    try:
        # Декодируем рефреш-токен, чтобы получить user_id
        user_id = decode_jwt_token(refresh_token)

        # Генерируем новый access-токен
        new_access_token = create_jwt_token(user_id=user_id)

        return RefreshTokenRequest(access_token=new_access_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


