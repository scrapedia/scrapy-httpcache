from typing import TypeVar

from scrapy.crawler import Crawler
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector

TCrawler = TypeVar("TCrawler", bound=Crawler)
TException = TypeVar("TException", bound=Exception)
TRequest = TypeVar("TRequest", bound=Request)
TResponse = TypeVar("TResponse", bound=Response)
TSpider = TypeVar("TSpider", bound=Spider)
TStatsCollector = TypeVar("TStatsCollector", bound=StatsCollector)
