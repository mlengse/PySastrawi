from abc import ABC, abstractmethod

class CacheInterface(ABC):
    """Interface for a cache storing word-to-stem mappings."""

    @abstractmethod
    def has(self, key):
        ...

    @abstractmethod
    def set(self, key, value):
        ...

    @abstractmethod
    def get(self, key):
        ...
