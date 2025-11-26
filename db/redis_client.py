# db/redis_client.py
import os
import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# единый клиент для приложения (async)
redis_client: aioredis.Redis | None = None

def get_redis_client() -> aioredis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis_client
