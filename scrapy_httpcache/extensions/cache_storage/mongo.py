"""
The mongo cache storage
"""
import logging
import re
from typing import Optional

from motor.core import AgnosticClient as AsyncIOMotorClient
from motor.core import AgnosticCollection as AsyncIOMotorCollection
from motor.core import AgnosticDatabase as AsyncIOMotorDatabase
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from scrapy.settings import Settings

from scrapy_httpcache import TRequest, TResponse, TSpider
from scrapy_httpcache.extensions.cache_storage import CacheStorage

logger = logging.getLogger(__name__)
pattern = re.compile("^HTTPCACHE_MONGO_MONGOCLIENT_(?P<kwargs>(?!KWARGS).*)$")


class MongoCacheStorage(CacheStorage):
    """
    The sync mongo cache storage with pymongo
    """

    def __init__(self, settings: Settings):
        super(MongoCacheStorage, self).__init__(settings)

        self.settings = settings
        self.mongo_settings = {
            pattern.sub(lambda x: x.group(1).lower(), k): v
            for k, v in filter(
                lambda pair: pattern.match(pair[0]), settings.copy_to_dict().items()
            )
        }
        self.mongo_settings.update(self.settings["HTTPCACHE_MONGO_MONGOCLIENT_KWARGS"])

        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None

    def open_spider(self, spider: TSpider) -> None:
        """

        :param spider:
        :type spider: TSpider
        :return:
        :rtype: None
        """
        # TODO: connect to the database
        self.client: MongoClient = MongoClient(**self.mongo_settings)
        self.db: Database = self.client.get_database(
            **get_arguments(self.settings["HTTPCACHE_MONGO_DATABASE"])
        )
        self.collection: Collection = self.db.get_collection(
            **get_arguments(self.settings["HTTPCACHE_MONGO_COLLECTION"])
        )
        self.collection.create_index([("key", ASCENDING)], unique=True)

        logger.debug("Using MongoDB cache storage", extra={"spider": spider})

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
