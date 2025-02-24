import jwt
from datetime import datetime, timedelta
from core.config import settings
from cache.redis.redis_requests import get_code , delete_code
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = settings.AUTH_SECRET_KEY

def create_jwt_token(user_id: int) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)
    token_data = {"sub": str(user_id), "exp": expiration}
    return jwt.encode(token_data, settings.AUTH_SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=["HS256"])
        return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")




def generate_sms_code() -> str:
    from random import randint
    return str(randint(100000, 999999))

async def verify_sms_code(phone: str, entered_code: str) -> bool:
    """
    Сверяет введенный код с кодом, сохранённым в Redis.
    Возвращает True, если коды совпадают, иначе False.
    """
    stored_code = await get_code(phone)
    if stored_code is None:
        raise ValueError("Code has expired or does not exist")
    if stored_code.decode() == entered_code:
        await delete_code(phone)
        return True
    return False