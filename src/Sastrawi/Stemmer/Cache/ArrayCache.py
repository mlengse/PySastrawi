from Sastrawi.Stemmer.Cache.CacheInterface import CacheInterface
from collections import OrderedDict

class ArrayCache(CacheInterface):
    """In-memory cache with LRU eviction policy"""

    def __init__(self, max_size=100000):
        self.data = OrderedDict()
        self.max_size = max_size

    def set(self, key, value):
        if key in self.data:
            del self.data[key]
        self.data[key] = value

        while len(self.data) > self.max_size:
            self.data.popitem(last=False)

    def get(self, key):
        if key in self.data:
            value = self.data[key]
            del self.data[key]
            self.data[key] = value
            return value

    def has(self, key):
        return key in self.data
