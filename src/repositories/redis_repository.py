from redis import Redis

class RedisRepository:

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def set_value(self, key:str, value:str):
        self.redis.set(key, value)

    def get_value(self, key:str) -> str:
        return self.redis.get(key)