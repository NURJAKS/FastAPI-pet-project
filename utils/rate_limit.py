import redis.asyncio as aioredis
from fastapi import HTTPException

redis = aioredis.from_url("redis://localhost:6379", decode_responses=True)

async def rate_limit(key: str, limit: int, seconds: int):
    """
    Простая система rate limiting:
    - key: уникальный идентификатор (email/ip/user_id)
    - limit: сколько попыток разрешено
    - seconds: окно времени
    """

    attempts = await redis.incr(key)

    if attempts == 1:
        await redis.expire(key, seconds)

    if attempts > limit:
        raise HTTPException(
            status_code=429,
            detail="Too many attempts. Please try again later."
        )
