import logging
from redis import Redis

logger = logging.getLogger("uvicorn.log")


def get_redis_client():
    redis_client = Redis(host="127.0.0.1", port=6379)
    try:
        redis_client.ping()
        logger.info("Connected to Redis!")
    except Exception as e:
        logger.error(f"Error connecting to Redis: {e}")

    try:
        yield redis_client
    finally:
        redis_client.close()


def create_redis_key(collection: str, key: str) -> str:
    return f"{collection}_{key}"
