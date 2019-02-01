import scrapy
from scrapy.http import Request
from urllib import parse

from scrapy.loader import ItemLoader

from Scrapy.items import HBProductItem


class Hb_museumSpider(scrapy.Spider):
    name = "hb_museum"
    allowed_domains = ['www.hbww.org']
    start_urls = ['http://www.hbww.org/Views/ArtGoods.aspx?PNo=Winchance&No=ZBCP&type=List']

    def parse(self, response):
        item = response.css()