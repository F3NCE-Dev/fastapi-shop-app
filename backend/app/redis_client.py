from redis.asyncio import Redis
from app.config.config import settings

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis_client() -> Redis:
    return redis_client
