import functools


class LRUCache:
    """"""

    def __init__(self, size: int = 5):
        """"""
        self._size = size
        self._hash_map = {}
        self._timeline = []

    def cache(self, key, value):
        """"""
        if key in self._hash_map:
            # move key to front
            for i in range(len(self._timeline)):
                if key == self._timeline[i]:
                    self._timeline.pop(i)
                    self._timeline = [key] + self._timeline
                    return
            raise Exception("FATAL: cache is in invalid state")

        self._hash_map[key] = value
        self._timeline = [key] + self._timeline

        if len(self._hash_map.keys()) > self._size:
            key = self._timeline.pop()
            del self._hash_map[key]

    def lookup(self, key):
        """"""
        if key not in self._hash_map:
            # key not in cache
            return None

        return self._hash_map[key]


cache = LRUCache(5)


def lru_cache(func):
    """"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (
            ",".join([str(arg) for arg in args])
            + ","
            + ",".join([f"{key}={value}" for key, value in kwargs.items()])
        )

        value = cache.lookup(key)

        if value is None:
            value = func(*args, **kwargs)
            cache.cache(key, value)

        return value

    return wrapper
