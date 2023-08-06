from sdkboil.api_context import ApiContext
from .lib.constants import CHAINSIDE_SANDBOX_API_HOSTAME, CHAINSIDE_API_HOSTNAME
from .lib.cache import CacheAdapterFactory


class ChainsideApiContext(ApiContext):
    def __init__(self, config):
        hostname = CHAINSIDE_API_HOSTNAME if config['mode'] == 'live' else CHAINSIDE_SANDBOX_API_HOSTAME
        config['version'] = 'v1'
        config['token_cache_key'] = '___chainside.access.token___'
        cache = CacheAdapterFactory(config).get()
        super().__init__(hostname, config, cache)
