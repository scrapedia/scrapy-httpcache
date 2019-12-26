import dbm
import logging
import os
import pickle
from dbm.dumb import _Database
from importlib import import_module
from time import time
from typing import Dict, Optional, Union

from scrapy.http.headers import Headers
from scrapy.responsetypes import responsetypes
from scrapy.settings import Settings
from scrapy.utils.project import data_path

from scrapy_httpcache import TRequest, TResponse, TSpider
from scrapy_httpcache.extensions.cache_storage import CacheStorage

logger = logging.getLogger(__name__)


class DbmCacheStorage(CacheStorage):
    def __init__(self, settings: Settings):
        super(DbmCacheStorage, self).__init__(settings)
        self.cachedir = data_path(settings["HTTPCACHE_DIR"], createdir=True)
        self.dbmodule: dbm = import_module(settings["HTTPCACHE_DBM_MODULE"])
        self.db: _Database = None

    def open_spider(self, spider: TSpider) -> None:
        dbpath = os.path.join(self.cachedir, "%s.db" % spider.name)
        self.db = self.dbmodule.open(dbpath, "c")

        logger.debug(
            "Using DBM cache storage in %(cachepath)s" % {"cachepath": dbpath},
            extra={"spider": spider},
        )

    def close_spider(self, spider: TSpider) -> None:
        self.db.close()

    def retrieve_response(
        self, spider: TSpider, request: TRequest
    ) -> Optional[TResponse]:
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
        key = self._request_key(request)
        data = {
            "status": response.status,
            "url": response.url,
            "headers": dict(response.headers),
            "body": response.body,
        }
        self.db["%s_data" % key] = pickle.dumps(data, protocol=2)
        self.db["%s_time" % key] = str(time())

    def _read_data(
        self, spider: TSpider, request: TRequest
    ) -> Optional[Dict[str, Union[int, str, bytes, Dict]]]:
        key = self._request_key(request)
        db = self.db
        tkey = "%s_time" % key
        if tkey not in db:
            return  # not found

        ts = db[tkey]
        if 0 < self.expiration_secs < time() - float(ts):
            return  # expired

        return pickle.loads(db["%s_data" % key])
