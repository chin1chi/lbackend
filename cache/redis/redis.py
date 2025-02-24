from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING
from cache.serialize import AbstractSerializer, PickleSerializer

from core.config import settings # Импортируем настройки из config
from redis.asyncio import ConnectionPool, Redis

if TYPE_CHECKING:
    from datetime import timedelta
    from typing import Any, Callable

DEFAULT_TTL = 10


# Создаем экземпляр настроек CacheSettings


# Инициализация Redis клиента с использованием значений из CacheSettings
redis_client = Redis(
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASS,
        db=0,
    ),
)

def build_key(*args: tuple[str, Any], **kwargs: dict[str, Any]) -> str:
    args_str = ":".join(map(str, args))
    kwargs_str = ":".join(f"{key}={value}" for key, value in kwargs.items())
    return f"{args_str}:{kwargs_str}"

async def set_redis_value(
    key: bytes | str, value: bytes | str, ttl: int | timedelta | None = DEFAULT_TTL, is_transaction: bool = False
) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipeline:
        await pipeline.set(key, value)
        if ttl:
            await pipeline.expire(key, ttl)
        await pipeline.execute()

def cached(
    ttl: int | timedelta = DEFAULT_TTL,
    namespace: str = "main",
    cache: Redis = redis_client,
    key_builder: Callable[..., str] = build_key,
    serializer: AbstractSerializer | None = None,
) -> Callable:
    if serializer is None:
        serializer = PickleSerializer()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: tuple[str, Any], **kwargs: dict[str, Any]) -> Any:
            key = key_builder(*args, **kwargs)
            key = f"{namespace}:{func.__module__}:{func.__name__}:{key}"

            # Check if the key is in the cache
            cached_value = await cache.get(key)
            if cached_value is not None:
                return serializer.deserialize(cached_value)

            # If not in cache, call the original function
            result = await func(*args, **kwargs)

            # Store the result in Redis
            await set_redis_value(
                key=key,
                value=serializer.serialize(result),
                ttl=ttl,
            )

            return result

        return wrapper

    return decorator

async def clear_cache(
    func: Callable,
    *args: Any,
    **kwargs: Any,
) -> None:
    namespace: str = kwargs.get("namespace", "main")
    key = build_key(*args, **kwargs)
    key = f"{namespace}:{func.__module__}:{func.__name__}:{key}"
    await redis_client.delete(key)

