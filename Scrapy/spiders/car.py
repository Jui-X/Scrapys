# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader

from Scrapy.items import CarItem


class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['pcauto.com.cn']
    start_urls = ['https://price.pcauto.com.cn/comment/sg3524/p15.html']

    def parse(self, response):
        urls = response.css('#pcauto_page a::attr(href)').extract()
        for i in range(2, 9):
            base_url = "https:"
            yield Request(url=parse.urljoin(base_url, urls[i]), callback=self.parse_detailed)

    def parse_detailed(self, response):
        tag = response.css('.dianPing .conLit b::text').extract()
        comments = response.css('.dianPing .conLit span::text').extract()

        for i in range(0, 100):
            car_item = CarItem()
            car_item["tag"] = tag[i].replace("：", "")
            car_item["comment"] = comments[i]

            yield car_item




