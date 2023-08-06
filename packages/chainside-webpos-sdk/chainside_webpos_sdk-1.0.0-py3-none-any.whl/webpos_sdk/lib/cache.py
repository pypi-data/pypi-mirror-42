from sdkboil.cache import CacheAdapter

from .constants import DICT_CACHE, REDIS_CACHE, DJANGO_CACHE


class ChainsideCacheAdapter(CacheAdapter):
    def __getattr__(self, item):
        return getattr(self.cache, item)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        return self.cache.set(key, value)

    def delete(self, key):
        return self.cache.delete(key)


class RedisCacheAdapter(ChainsideCacheAdapter):
    def __init__(self, conf, *args, **kwargs):
        self.hostname = conf.get('hostname', 'localhost')
        self.port = conf.get('port', 6379)
        self.password = conf.get('password', None)
        self.decode = conf.get('decode_responses', True)
        try:
            from redis import Redis
            self.cache = Redis(host=self.hostname, port=self.port,
                               password=self.password, decode_responses=self.decode)
        except ImportError:
            raise ImportError(
                "redis cache adapter configured but redis could not be imported")


class DjangoCacheAdapter(ChainsideCacheAdapter):
    def __init__(self):
        try:
            from django.core.cache import cache
            self.cache = cache
        except ImportError:
            raise ImportError(
                "django cache adapter is configured but django could not be imported")


class DictCacheAdapter(ChainsideCacheAdapter):
    __cache = None

    def __new__(cls, *args, **kwargs):
        if cls.__cache is None:
            cls.__cache = object.__new__(cls)
        return cls.__cache

    def __init__(self):
        self.cache = {}

    def get(self, key):
        try:
            return self.cache[key]
        except KeyError:
            return None

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        try:
            del self.cache[key]
        except KeyError:
            pass


class CacheAdapterFactory(object):
    _ADAPTERS = {DICT_CACHE: DictCacheAdapter,
                 REDIS_CACHE: RedisCacheAdapter,
                 DJANGO_CACHE: DjangoCacheAdapter}

    def __init__(self, config):
        self.config = config

    def get(self):
        try:
            adapter = self.config['cache_conf']['driver']
        except KeyError:
            return self._ADAPTERS[DICT_CACHE]()
        try:
            return self._ADAPTERS[adapter](self.config['cache_conf'])
        except KeyError:
            raise ValueError(
                "Unknown cache adapter {}, configurable adapters are {}".format(adapter, list(self._ADAPTERS.keys())))
