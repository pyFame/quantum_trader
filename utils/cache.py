
from cachetools import TTLCache

class Cache:
    def __init__(self, ttl:int=None,maxsize:int=None): # ttl - 1 hr, 128
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        self.cache.pop(key, None)

    def clear(self):
        self.cache.clear()

    def __repr__(self):
        return f"Cache({self.cache})"

    def __str__(self):
        return self.cache

    def __call__(self):
      return self.cache
