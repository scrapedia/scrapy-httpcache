"""
The metaclass for policy
"""
from abc import ABCMeta

from scrapy.settings import Settings

from scrapy_httpcache import TRequest, TResponse


class Policy(metaclass=ABCMeta):
    """
    The metaclass for policy
    """

    def __init__(self, settings: Settings):
        """

        :param settings:
        :type settings: Settings
        """

    def should_cache_request(self, request: TRequest) -> bool:
        """

        :param request:
        :type request: TRequest
        :return:
        :rtype: bool
        """

    def should_cache_response(self, response: TResponse, request: TRequest) -> bool:
        """

        :param response:
        :type response: TResponse
        :param request:
        :type request: TRequest
        :return:
        :rtype: bool
        """

    def is_cached_response_fresh(
        self, cachedresponse: TResponse, request: TRequest
    ) -> bool:
        """

        :param cachedresponse:
        :type cachedresponse: TResponse
        :param request:
        :type request: TRequest
        :return:
        :rtype: bool
        """

    def is_cached_response_valid(
        self, cachedresponse: TResponse, response: TResponse, request: TRequest
    ) -> bool:
        """

        :param cachedresponse:
        :type cachedresponse: TResponse
        :param response:
        :type response: TResponse
        :param request:
        :type request: TRequest
        :return:
        :rtype: bool
        """
