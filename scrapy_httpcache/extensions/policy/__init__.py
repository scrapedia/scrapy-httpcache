"""
The metaclass for policy
"""
from abc import ABCMeta

from scrapy.settings import Settings

from scrapy_httpcache import TRequest


class Policy(metaclass=ABCMeta):
    """
    The metaclass for policy
    """

    def __init__(self, settings: Settings):
        """

        :param settings:
        :type settings: Settings
        """

    def should_cache_request(self, request: TRequest):
        """

        :param request:
        :type request: TRequest
        """

    def should_cache_response(self, response, request):
        """

        :param response:
        :type response: TResponse
        :param request:
        :type request: TRequest
        """

    def is_cached_response_fresh(self, cachedresponse, request):
        """

        :param cachedresponse:
        :type cachedresponse: TResponse
        :param request:
        :type request: TRequest
        """

    def is_cached_response_valid(self, cachedresponse, response, request):
        """

        :param cachedresponse:
        :type cachedresponse: TResponse
        :param response:
        :type response: TResponse
        :param request:
        :type request: TRequest
        """
