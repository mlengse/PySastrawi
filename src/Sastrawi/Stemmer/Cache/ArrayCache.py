from Sastrawi.Stemmer.Cache.CacheInterface import CacheInterface
from collections import OrderedDict
from threading import Lock

class ArrayCache(CacheInterface):
    """In-memory cache with LRU eviction policy, safe for concurrent use."""

    def __init__(self, max_size=100000):
        self.data = OrderedDict()
        self.max_size = max_size
        self._lock = Lock()

    def set(self, key, value):
        with self._lock:
            if key in self.data:
                del self.data[key]
            self.data[key] = value

            while len(self.data) > self.max_size:
                self.data.popitem(last=False)

    def get(self, key):
        with self._lock:
            if key in self.data:
                value = self.data[key]
                del self.data[key]
                self.data[key] = value
                return value

    def has(self, key):
        with self._lock:
            return key in self.data
