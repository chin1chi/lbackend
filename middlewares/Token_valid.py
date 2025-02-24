from fastapi import Request, HTTPException,Depends
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
from starlette.responses import Response
from utils.auth_utils import decode_jwt_token


class TokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        excluded_paths=["/docs","/redoc","/openapi.json","/auth"]
        if any(request.url.path.startswith(path) for path in excluded_paths):
            return await call_next(request)
        # Получаем токен из заголовка Authorization
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Token is missing")

        # Убираем "Bearer" из заголовка
        token = token.split(" ")[1] if " " in token else token

        try:

            user_id = decode_jwt_token(token)
            # Сохраняем user_id в request.state для дальнейшего использования
            request.state.user_id = user_id
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

        # Продолжаем выполнение запроса
        response = await call_next(request)
        return response

def get_current_user_id(request: Request)-> int :
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="User ID not found in request")
    return user_id

