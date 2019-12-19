from abc import ABCMeta, abstractmethod


class CacheStorage(metaclass=ABCMeta):
    def __init__(self, settings):
        """

        """

    @abstractmethod
    def open_spider(self, spider):
        """

        """

    @abstractmethod
    def close_spider(self, spider):
        """

        """

    @abstractmethod
    def retrieve_response(self, spider, request):
        """

        """

    @abstractmethod
    def store_response(self, spider, request, response):
        """

        """
