"""
The mongo cache storage
"""
import logging
import re
from datetime import datetime
from time import time
from typing import Dict, Optional, Union

from motor.core import AgnosticClient as AsyncIOMotorClient
from motor.core import AgnosticCollection as AsyncIOMotorCollection
from motor.core import AgnosticDatabase as AsyncIOMotorDatabase
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from scrapy.http.headers import Headers
from scrapy.responsetypes import responsetypes
from scrapy.settings import Settings
from scrapy.utils.python import to_unicode

from scrapy_httpcache import TRequest, TResponse, TSpider
from scrapy_httpcache.extensions.cache_storage import CacheStorage

logger = logging.getLogger(__name__)
pattern = re.compile("^HTTPCACHE_MONGO_MONGOCLIENT_(?P<kwargs>(?!KWARGS).*)$")


def get_arguments(var):
    return {str: {"name": var}, dict: var}[type(var)]


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
        data = self._read_data(spider, request)
        if data is None:
            return  # not cached
        url = data["url"]
        status = data["status"]
        headers = Headers(data["headers"])
        body = data["body"]
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

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
        data = {
            "status": response.status,
            "url": response.url,
            "headers": response.headers.to_unicode_dict(),
            "body": response.body,
        }
        data_for_human = {
            "status": response.status,
            "url": response.url,
            "headers": self._convert_headers(response),
            "body": response.text,
        }
        key = self._request_key(request)
        self.collection.update_one(
            {"key": key},
            {
                "$set": {
                    "data": data,
                    "data_for_human": data_for_human,
                    "key": key,
                    "time": datetime.utcnow(),
                }
            },
            upsert=True,
        )

    def _read_data(
        self, spider: TSpider, request: TRequest
    ) -> Optional[Dict[str, Union[int, str, bytes, Dict]]]:
        key = self._request_key(request)

        v = self.collection.find_one({"key": key}, {"data": True, "time": True})

        if not v:
            return  # not found

        if 0 < self.expiration_secs < time() - v["time"].timestamp():
            return  # expired

        return v["data"]

    def _convert_headers(self, response: TResponse):
        encoding = response.headers.encoding
        headers = response.headers.to_unicode_dict()

        set_cookie = []
        for cookie in [
            to_unicode(i, encoding) for i in response.headers.getlist("set-cookie")
        ]:
            cookie_ = {}
            for j in cookie.split(";"):
                key, value = j.split("=", 1)
                cookie_[key.strip()] = value.strip()
            if "expires" in cookie_:
                cookie_["expires"] = datetime.strptime(
                    cookie_["expires"], "%a, %d %b %Y %H:%M:%S %Z"
                )
            set_cookie.append(cookie_)
        headers["set-cookie"] = set_cookie

        if "date" in headers:
            headers["date"] = datetime.strptime(
                headers["date"], "%a, %d %b %Y %H:%M:%S %Z"
            )

        return headers


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
