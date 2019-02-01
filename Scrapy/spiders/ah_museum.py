import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader

from Scrapy.items import AHProductItem


class Nj_museumSpider(scrapy.Spider):
    name = "ah_museum"
    allowed_domains = ['www.ahm.cn']
    start_urls = ['http://www.ahm.cn/Service/ArtGoods/whcycp#page=1']

    def parse(self, response):
        items = response.css('.wclist .list ul li .imgbox::attr(href)').extract()
        base_url = "http://www.ahm.cn"
        for item in items:
            yield Request(url=parse.urljoin(base_url, item), callback=self.parse_detailed)

        next_url = response.css('#pager ul li a::attr(href)').extract()[-2]
        if next_url:
            yield Request(url=parse.urljoin(base_url, next_url), callback=self.parse)

    def parse_detailed(self, response):
        product_item = AHProductItem()

        name = response.css('.maindetail .title h1::text').extract()
        specification = response.css('.maindetail .cont p::text').extract()[0].split('：')
        specification = specification[1]
        introduction = response.css('.maindetail .cont p::text').extract()[-1]
        img_url = response.css('.wcdetail .imgfull a img::attr(src)').extract()

        item_loader = ItemLoader(item=AHProductItem(), response=response)
        item_loader.add_value("name", name)
        item_loader.add_value("specification", specification)
        item_loader.add_value("introduction", introduction)
        item_loader.add_value("img_url", img_url)

        product_item = item_loader.load_item()

        yield product_item
