import redis.asyncio as aioredis
from redis.asyncio.client import Redis
from config.redis_config import redis_config


class RedisClient:
    """Redis client to interact with Redis"""

    _redis_client: Redis = None

    @staticmethod
    async def connect():
        """Connect to Redis"""
        if RedisClient._redis_client:
            print("Redis client already connected")
            return

        print("Connecting to Redis...")
        RedisClient._redis_client = aioredis.from_url(
            url=f"redis://{redis_config.REDIS_HOST}:{redis_config.REDIS_PORT}",
            password=redis_config.REDIS_PASSWORD,
            db=redis_config.REDIS_DB,
            decode_responses=True,
        )
        print("Connected to Redis!")

    @staticmethod
    async def set(key, value):
        """Set the value at key"""
        await RedisClient._redis_client.set(key, value)

    @staticmethod
    async def get(key):
        """Get the value at key"""
        return await RedisClient._redis_client.get(key)

    @staticmethod
    async def delete(key):
        """Delete the value at key"""
        await RedisClient._redis_client.delete(key)

    @staticmethod
    async def exists(key):
        """Check if key exists"""
        return await RedisClient._redis_client.exists(key)

    @staticmethod
    async def close():
        """Close the connection"""
        if RedisClient._redis_client:
            print("Closing Redis client...")
            await RedisClient._redis_client.aclose()
            RedisClient._redis_client = None
            print("Redis client closed")
        else:
            print("Redis client already closed")
