from typing import Annotated
from urllib.request import Request

from fastapi import APIRouter, HTTPException, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection_to_db.database import get_async_session
from schemas.token_schemas import TokenRequest
from utils.auth_utils import create_jwt_token, generate_sms_code, verify_sms_code
from cache.redis.redis_requests import store_code
from schemas.auth_schemas import PhoneLoginRequest, CodeVerificationRequest
from database.request_to_db.database_requests import get_user_by_phone, create_user,create_player_for_user
from fastapi.security.api_key import APIKeyHeader
router = APIRouter()


@router.post("/login")
async def login_or_create_user(data: PhoneLoginRequest, db: AsyncSession = Depends(get_async_session)):
    # Проверяем, существует ли пользователь
    user = await get_user_by_phone(data.phone, db)
    if user is None:
        # Создаём нового пользователя
        user = await create_user(data.phone, db)

        # Проверяем, связан ли пользователь с партнёрами, и создаём игрока, если нужно
        await create_player_for_user(user, db)

    # Генерируем токен
    token = create_jwt_token(user.id)
    return TokenRequest(token=token)

@router.post("/send_code")
async def send_code(data: PhoneLoginRequest):
    code = generate_sms_code()
    await store_code(data.phone, code)
    # Тут добавить отправку SMS через внешний сервис
    return {"message": "Code sent"}


@router.post("/verify-code")
async def verify_code(data: CodeVerificationRequest):
    try:
        is_valid = await verify_sms_code(data.phone, data.entered_code)
        if is_valid:
            return {"message": "Code verified successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid code")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

authorization_token_key=APIKeyHeader(name="Authorization", auto_error=False)

def get_current_token(authorization_token: str = Security(authorization_token_key))->str:
    return authorization_token