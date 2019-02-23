import scrapy
import re
from scrapy.http import Request
from urllib import parse

from Scrapy.items import DoubanBookReviewItem
from scrapy.loader import ItemLoader


class DoubanSpider(scrapy.Spider):
    name = 'douban_review'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']

    def parse(self, response):
        tags = response.css('.tagCol tr td a::attr(href) ').extract()
        douban_url = "https://book.douban.com"
        for tag in tags:
            yield Request(url=parse.urljoin(douban_url, tag), callback=self.parse_tag)

    def parse_tag(self, response):
        # 获取编程标签下的书籍url并交给scrapy下载后进行解析
        post_nodes = response.css('.subject-item .info')
        for post_node in post_nodes:
            book_info = post_node.css('.pub::text').extract()
            # rating_nums = post_node.css('.star .rating_nums::text').extract_first('')
            post_url = post_node.css('h2 a::attr(href)').extract_first('')
            douban_id = post_url.split('/', 5)[-2]
            yield Request(url=post_url, meta={"book_info": book_info, "douban_id": douban_id}, dont_filter=True, callback=self.parse_detailed)

        # next_url = response.css('.next a::attr(href)').extract_first("")
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detailed(self, response):

        douban_id = response.meta["douban_id"]

        rating = response.css('.rating_self strong::text').extract()[0].strip()
        reviews = response.css('.review-list .review-item h2 a::attr(href)').extract()
        for i in range(0, 5):
            # enter the review_url to crawl reviews
            yield Request(url=reviews[i], meta={"douban_id": douban_id, "rating": rating}, dont_filter=True, callback=self.review_detailed)

    def review_detailed(self, response):
        review_item = DoubanBookReviewItem()

        douban_id = response.meta["douban_id"]
        rating = response.meta["rating"]
        review_content = response.css('.review-content::text').extract()
        review_content[0].replace('\n', '').replace('\t', '').replace('\xa0', '').strip()

        item_loader = ItemLoader(item=DoubanBookReviewItem(), response=response)
        item_loader.add_value("review", review_content)
        item_loader.add_value("douban_id", douban_id)
        item_loader.add_value("rating", rating)

        review_item = item_loader.load_item()

        yield review_item
