import directory_client_core.base
from directory_client_core.helpers import fallback

from django.core.cache import caches

from directory_api_client.version import __version__


class AbstractAPIClient(directory_client_core.base.AbstractAPIClient):

    version = __version__

    @fallback(cache=caches['api_fallback'])
    def fallback_cache_get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get(self, *args, use_fallback_cache=False, **kwargs):
        if use_fallback_cache:
            return self.fallback_cache_get(*args, **kwargs)
        return super().get(*args, **kwargs)
