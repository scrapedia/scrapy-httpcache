"""
The mongo cache storage
"""
import logging
from typing import Optional

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from scrapy.settings import Settings

from scrapy_httpcache import TRequest, TResponse, TSpider
from scrapy_httpcache.extensions.cache_storage import CacheStorage

logger = logging.getLogger(__name__)


class MongoCacheStorage(CacheStorage):
    """
    The sync mongo cache storage with pymongo
    """

    def __init__(self, settings: Settings):
        super(MongoCacheStorage, self).__init__(settings)

        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None

    def open_spider(self, spider: TSpider) -> None:
        """

        :param spider:
        :type spider: TSpider
        """
        # TODO: connect to the database

    def close_spider(self, spider: TSpider) -> None:
        """

        :param spider:
        :type spider: TSpider
        """
        self.client.close()

    def retrieve_response(
        self, spider: TSpider, request: TRequest
    ) -> Optional[TResponse]:
        """

        :param spider:
        :type spider: TSpider
        :param request:
        :type request: TRequest
        """

    def store_response(
        self, spider: TSpider, request: TRequest, response: TResponse
    ) -> None:
        """

        :param spider:
        :type spider: TSpider
        :param request:
        :type request: TRequest
        :param response:
        :type response: TResponse
        """


class MongoAsyncCacheStorage(CacheStorage):
    """
    The async mongo cache storage with motor
    """

    def __init__(self, settings: Settings):
        super(MongoAsyncCacheStorage, self).__init__(settings)

        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.collection: Optional[AsyncIOMotorCollection] = None

    def open_spider(self, spider: TSpider) -> None:
        """

        :param spider:
        :type spider: TSpider
        """

    def close_spider(self, spider: TSpider) -> None:
        """

        :param spider:
        :type spider: TSpider
        """
        self.client.close()

    def retrieve_response(
        self, spider: TSpider, request: TRequest
    ) -> Optional[TResponse]:
        """

        :param spider:
        :type spider: TSpider
        :param request:
        :type request: TRequest
        """

    def store_response(
        self, spider: TSpider, request: TRequest, response: TResponse
    ) -> None:
        """

        :param spider:
        :type spider: TSpider
        :param request:
        :type request: TRequest
        :param response:
        :type response: TResponse
        """
