# File name: redis_repository.py
from redis import Redis

from src.interfaces.redis_repository_interface import IRedisRepository


class RedisRepository(IRedisRepository):

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def set_value(self, key: str, value: str) -> None:
        self.redis.set(key, value)

    def get_value(self, key: str) -> str:
        value = self.redis.get(key)
        return value
