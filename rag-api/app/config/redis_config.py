import os
from dotenv import load_dotenv

load_dotenv(override=True)


class RedisConfig:
    """
    Configurations to connect with AWS Services
    """

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    REDIS_EXPIRY = int(os.getenv("REDIS_EXPIRY", "3600"))
    if REDIS_PASSWORD:
        REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    else:
        REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    print(REDIS_HOST)

redis_config = RedisConfig()
