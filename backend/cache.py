import redis
from os import getenv

REDIS_URL = getenv("REDIS_URL") or "redis://localhost:6379/0"
REDIS = redis.Redis.from_url(REDIS_URL, decode_responses=True)
