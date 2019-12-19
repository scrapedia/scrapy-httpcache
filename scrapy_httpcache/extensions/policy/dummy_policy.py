import logging

from scrapy.utils.httpobj import urlparse_cached

logger = logging.getLogger(__name__)


class DummyPolicy(object):
    def __init__(self, settings):
        self.ignore_schemes = settings.getlist("HTTPCACHE_IGNORE_SCHEMES")
        self.ignore_http_codes = [
            int(x) for x in settings.getlist("HTTPCACHE_IGNORE_HTTP_CODES")
        ]

    def should_cache_request(self, request):
        return urlparse_cached(request).scheme not in self.ignore_schemes

    def should_cache_response(self, response, request):
        return response.status not in self.ignore_http_codes

    def is_cached_response_fresh(self, cachedresponse, request):
        return True

    def is_cached_response_valid(self, cachedresponse, response, request):
        return True
