import logging
from redis import Redis

logger = logging.getLogger("uvicorn.log")


def get_redis_client():
    """
    Used to inject redis connection within API route endpoints.
    """
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
    """
    Creates a redis key by combining the collection name with the item key.

    :param collection (str): Name of collection in redis cache
    :param key (str): Unique ID of item within collection. This is the session_id.
    :returns: returns the key for a specific item within a collection.
    """
    return f"{collection}_{key}"
