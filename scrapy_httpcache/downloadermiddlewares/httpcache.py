from __future__ import annotations

from email.utils import formatdate
from typing import Optional, Tuple, Union

from scrapy import signals
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.settings import Settings
from scrapy.utils.misc import load_object
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from twisted.web.client import ResponseFailed

from scrapy_httpcache import (
    TCrawler,
    TException,
    TRequest,
    TResponse,
    TSpider,
    TStatsCollector,
)
from scrapy_httpcache.extensions.httpcache import (
    DbmCacheStorage,
    DummyPolicy,
    FilesystemCacheStorage,
    RFC2616Policy,
)


class HttpCacheMiddleware(object):

    DOWNLOAD_EXCEPTIONS: Tuple = (
        defer.TimeoutError,
        TimeoutError,
        DNSLookupError,
        ConnectionRefusedError,
        ConnectionDone,
        ConnectError,
        ConnectionLost,
        TCPTimedOutError,
        ResponseFailed,
        IOError,
    )

    def __init__(self, settings: Settings, stats: TStatsCollector) -> None:
        if not settings.getbool("HTTPCACHE_ENABLED"):
            raise NotConfigured
        self.policy: Union[DummyPolicy, RFC2616Policy] = load_object(
            settings["HTTPCACHE_POLICY"]
        )(settings)
        self.storage: Union[DbmCacheStorage, FilesystemCacheStorage] = load_object(
            settings["HTTPCACHE_STORAGE"]
        )(settings)
        self.ignore_missing: bool = settings.getbool("HTTPCACHE_IGNORE_MISSING")
        self.stats: TStatsCollector = stats

    @classmethod
    def from_crawler(cls, crawler: TCrawler) -> HttpCacheMiddleware:
        o: HttpCacheMiddleware = cls(crawler.settings, crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider: TSpider) -> None:
        self.storage.open_spider(spider)

    def spider_closed(self, spider: TSpider) -> None:
        self.storage.close_spider(spider)

    def process_request(
        self, request: TRequest, spider: TSpider
    ) -> Optional[TResponse]:
        if request.meta.get("dont_cache", False):
            return

        # Skip uncacheable requests
        if not self.policy.should_cache_request(request):
            request.meta["_dont_cache"] = True  # flag as uncacheable
            return

        # Look for cached response and check if expired
        cachedresponse: TResponse = self.storage.retrieve_response(spider, request)
        if cachedresponse is None:
            self.stats.inc_value("httpcache/miss", spider=spider)
            if self.ignore_missing:
                self.stats.inc_value("httpcache/ignore", spider=spider)
                raise IgnoreRequest("Ignored request not in cache: %s" % request)
            return  # first time request

        # Return cached response only if not expired
        cachedresponse.flags.append("cached")
        if self.policy.is_cached_response_fresh(cachedresponse, request):
            self.stats.inc_value("httpcache/hit", spider=spider)
            return cachedresponse

        # Keep a reference to cached response to avoid a second cache lookup on
        # process_response hook
        request.meta["cached_response"] = cachedresponse

    def process_response(
        self, request: TRequest, response: TResponse, spider: TSpider
    ) -> TResponse:
        if request.meta.get("dont_cache", False):
            return response

        # Skip cached responses and uncacheable requests
        if "cached" in response.flags or "_dont_cache" in request.meta:
            request.meta.pop("_dont_cache", None)
            return response

        # RFC2616 requires origin server to set Date header,
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.18
        if "Date" not in response.headers:
            response.headers["Date"] = formatdate(usegmt=1)

        # Do not validate first-hand responses
        cachedresponse: Optional[TResponse] = request.meta.pop("cached_response", None)
        if cachedresponse is None:
            self.stats.inc_value("httpcache/firsthand", spider=spider)
            self._cache_response(spider, response, request, cachedresponse)
            return response

        if self.policy.is_cached_response_valid(cachedresponse, response, request):
            self.stats.inc_value("httpcache/revalidate", spider=spider)
            return cachedresponse

        self.stats.inc_value("httpcache/invalidate", spider=spider)
        self._cache_response(spider, response, request, cachedresponse)
        return response

    def process_exception(
        self, request: TRequest, exception: TException, spider: TSpider
    ) -> Optional[TResponse]:
        cachedresponse: TResponse = request.meta.pop("cached_response", None)
        if cachedresponse is not None and isinstance(
            exception, self.DOWNLOAD_EXCEPTIONS
        ):
            self.stats.inc_value("httpcache/errorrecovery", spider=spider)
            return cachedresponse

    def _cache_response(
        self,
        spider: TSpider,
        response: TResponse,
        request: TRequest,
        cachedresponse: Optional[TResponse],
    ) -> None:
        if self.policy.should_cache_response(response, request):
            self.stats.inc_value("httpcache/store", spider=spider)
            self.storage.store_response(spider, request, response)
        else:
            self.stats.inc_value("httpcache/uncacheable", spider=spider)
