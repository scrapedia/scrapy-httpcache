"""
The settings for httpcache
"""
from typing import List

HTTPCACHE_ENABLED = False
HTTPCACHE_IGNORE_MISSING = False

# ------------------------------------------------------------------------------
# DUMMY POLICY (ORIGINAL)
# ------------------------------------------------------------------------------
# HTTPCACHE_POLICY = "scrapy_httpcache.extensions.policy.dummy.DummyPolicy"
# HTTPCACHE_IGNORE_SCHEMES = ["file"]
# HTTPCACHE_IGNORE_HTTP_CODES = []

# ------------------------------------------------------------------------------
# RFC2616 POLICY (ORIGINAL)
# ------------------------------------------------------------------------------
HTTPCACHE_POLICY = "scrapy_httpcache.extensions.policy.rfc2616.RFC2616Policy"
HTTPCACHE_ALWAYS_STORE = False
HTTPCACHE_IGNORE_SCHEMES: List[str] = ["file"]
HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS = []

# ------------------------------------------------------------------------------
# DBM (ORIGINAL)
# ------------------------------------------------------------------------------
# HTTPCACHE_STORAGE = "scrapy_http.extensions.cache_storage.dbm.DbmCacheStorage"
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DBM_MODULE = "dbm"

# ------------------------------------------------------------------------------
# FILE SYSTEM (ORIGINAL)
# ------------------------------------------------------------------------------
# HTTPCACHE_STORAGE = (
#     "scrapy_httpcache.extensions.cache_storage.file_system.FilesystemCacheStorage"
# )
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_GZIP = False

# ------------------------------------------------------------------------------
# MONGODB
# http://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
# ------------------------------------------------------------------------------
HTTPCACHE_STORAGE = "scrapy_httpcache.extensions.cache_storage.mongo.MongoCacheStorage"

HTTPCACHE_EXPIRATION_SECS = 0

HTTPCACHE_MONGO_MONGOCLIENT_HOST = "localhost"
HTTPCACHE_MONGO_MONGOCLIENT_PORT = 27017
HTTPCACHE_MONGO_MONGOCLIENT_DOCUMENT_CLASS = dict
HTTPCACHE_MONGO_MONGOCLIENT_TZ_AWARE = False
HTTPCACHE_MONGO_MONGOCLIENT_CONNECT = True

HTTPCACHE_MONGO_MONGOCLIENT_KWARGS = {
    # 'username': 'username',
    # 'password': 'password',
    # 'authSource': 'admin',
    # 'authMechanism': 'SCRAM-SHA-1',
}

HTTPCACHE_MONGO_DATABASE = "cache_storage"
# or
# HTTPCACHE_MONGO_DATABASE = {
#     'name': 'cache_storage',
#     'codec_options': None,
#     'read_preference': None,
#     'write_concern': None,
#     'read_concern': None
# }

HTTPCACHE_MONGO_COLLECTION = "cache"
# or
# HTTPCACHE_MONGO_COLLECTION = {
#     'name': 'cache',
#     'codec_options': None,
#     'read_preference': None,
#     'write_concern': None,
#     'read_concern': None
# }
