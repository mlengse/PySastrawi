class CacheInterface:
    """Interface for a cache storing word-to-stem mappings."""

    def has(self, key):
        pass

    def set(self, key, value):
        pass

    def get(self, key):
        pass


