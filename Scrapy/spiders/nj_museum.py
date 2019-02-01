import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader

from Scrapy.items import NJProductItem


class Nj_museumSpider(scrapy.Spider):
    name = "nj_museum"
    allowed_domains = ['www.njmuseum.com']
    start_urls = ['http://www.njmuseum.com/html/Commodity_TypeFrame@isParent@@typeid@ROOT@page@1.html']

    def parse(self, response):
        items = response.css('.pub_right .shopclass .shop li a::attr(href)').extract()
        base_url = "http://www.njmuseum.com/html"
        for item in items:
            yield Request(url=parse.urljoin(base_url, item), callback=self.parse_detailed)

        next_url = response.css('.list_page tr td a::attr(href)').extract()[-2]
        if next_url:
            yield Request(url=parse.urljoin(base_url, next_url), callback=self.parse)

    def parse_detailed(self, response):
        product_item = NJProductItem()
        info = response.css('.shop_other li label::text').extract()
        img_url = response.css('.shop_show .shop_img img::attr(src)').extract()
        name = info[0]
        specification = info[1]
        texture = info[2]
        price = info[3]

        item_loader = ItemLoader(item=NJProductItem(), response=response)
        item_loader.add_value("name", name)
        item_loader.add_value("specification", specification)
        item_loader.add_value("texture", texture)
        item_loader.add_value("price", price)
        item_loader.add_value("img_url", img_url)

        product_item = item_loader.load_item()

        yield product_item
