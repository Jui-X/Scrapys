import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader

from Scrapy.items import ZHSProductItem


class ZHSSpider(scrapy.Spider):
    name = "zhs"
    allowed_domains = ['www.zhihuatemple.com']
    start_urls = ['http://www.zhihuatemple.com/MuseumSouvenir/']

    def parse(self, response):
        items = response.css('.li_cul .li_zhs_la ul li a::attr(href)').extract()
        base_url = "http://www.zhihuatemple.com"
        for item in items:
            yield Request(url=parse.urljoin(base_url, item), callback=self.parse_detailed)

        next_url = response.css('.page-btn a::attr(href)').extract()[-2]
        base_page_url = "http://www.zhihuatemple.com/MuseumSouvenir/"
        if next_url:
            yield Request(url=parse.urljoin(base_page_url, next_url), callback=self.parse)

    def parse_detailed(self, response):
        product_item = ZHSProductItem()

        
        