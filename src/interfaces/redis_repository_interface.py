# File name: redis_repository_interface.py
from abc import ABC, abstractmethod


class IRedisRepository(ABC):
    """Interface for RedisRepository"""

    @abstractmethod
    def set_value(self, key: str, value: str) -> None:
        """Set a value in Redis by key"""
        pass

    @abstractmethod
    def get_value(self, key: str) -> str:
        """Retrieve a value from Redis by key"""
        pass
