from redis import Redis
from config.redis_config import redis_config


class RedisClient:
    """Redis client to interact with Redis"""

    _redis_client: Redis = None

    @staticmethod
    def connect():
        """Connect to Redis"""
        if RedisClient._redis_client:
            print("Redis client already connected")
            return

        print("Connecting to Redis...")
        RedisClient._redis_client = Redis(
            host=redis_config.REDIS_HOST,
            port=redis_config.REDIS_PORT,
            password=redis_config.REDIS_PASSWORD,
            db=redis_config.REDIS_DB,
            decode_responses=True,
        )
        print("Current Redis Size", RedisClient._redis_client.dbsize())
        print("Connected to Redis!")

    @staticmethod
    def set(key, value):
        """Set the value at key"""
        RedisClient._redis_client.set(key, value, ex=redis_config.REDIS_EXPIRY)

    @staticmethod
    def get(key):
        """Get the value at key"""
        return RedisClient._redis_client.get(key)

    @staticmethod
    def delete(key):
        """Delete the value at key"""
        RedisClient._redis_client.delete(key)

    @staticmethod
    def exists(key):
        """Check if key exists"""
        return RedisClient._redis_client.exists(key)

    @staticmethod
    def close():
        """Close the connection"""
        if RedisClient._redis_client:
            print("Closing Redis client...")
            RedisClient._redis_client.close()
            RedisClient._redis_client = None
            print("Redis client closed")
        else:
            print("Redis client already closed")
