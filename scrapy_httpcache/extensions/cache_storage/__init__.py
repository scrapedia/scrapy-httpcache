"""
The metaclass of cache storage
"""
from abc import ABCMeta, abstractmethod

from scrapy.settings import Settings

from scrapy_httpcache import TRequest, TResponse, TSpider


class CacheStorage(metaclass=ABCMeta):
    """
    The metaclass of cache storage
    """

    def __init__(self, settings: Settings):
        """

        :param settings:
        :type settings: Settings
        """

    @abstractmethod
    def open_spider(self, spider: TSpider):
        """

        :param spider:
        :type spider: TSpider
        """

    @abstractmethod
    def close_spider(self, spider: TSpider):
        """

        :param spider:
        :type spider: TSpider
        """

    @abstractmethod
    def retrieve_response(self, spider: TSpider, request: TRequest):
        """

        :param spider:
        :type spider: TSpider
        :param request:
        :type request: TRequest
        """

    @abstractmethod
    def store_response(self, spider: TSpider, request: TRequest, response: TResponse):
        """

        :param spider:
        :type spider: TSpider
        :param request:
        :type request: TRequest
        :param response:
        :type response: TResponse
        """
