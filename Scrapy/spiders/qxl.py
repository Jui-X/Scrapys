import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader

from Scrapy.items import QXLProductItem


class QXLSpider(scrapy.Spider):
    name = "qxl"
    allowed_domains = ['ly.qingxiling.com']
    start_urls = ['http://ly.qingxiling.com/?p=577&city_name=']

    def parse(self, response):
        pages = response.css('.page_navigation #articeBottom a::attr(href)').extract()
        base_url = "http://ly.qingxiling.com"
        for page in pages:
            yield Request(url=parse.urljoin(base_url, page), callback=self.parse_page)

    def parse_page(self, response):
        items = response.css('.contentFy a::attr(href)').extract()
        base_url = "http://ly.qingxiling.com"
        for item in items:
            yield Request(url=parse.urljoin(base_url, item), callback=self.parse_detailed)

    def parse_detailed(self, response):
        name = response.css()


