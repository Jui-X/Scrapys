import MySQLdb
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from Scrapy.items import DoubanBookReviewItem


class DoubanSpider(scrapy.Spider):
    name = 'douban_book_review'
    allowed_domains = ['book.douban.com']

    def start_requests(self):

        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="scrapy_mysql", charset="utf8")
        cursor = conn.cursor()

        sql = """
                            SELECT douban_id FROM book 
                    """
        cursor.execute(sql)

        results = cursor.fetchall()
        urls = []
        for result in results:
            url = "https://book.douban.com/subject/" + str(result[0]) + "/"
            urls.append(url)

        conn.close()

        for start_url in urls:
            douban_id = start_url.split("/")[-2]
            yield scrapy.Request(url=start_url, meta={"douban_id": douban_id}, callback=self.parse)

    def parse(self, response):
        douban_id = response.meta["douban_id"]

        reviews = response.css('.review-list .review-item h2 a::attr(href)').extract()
        for i in range(0, 5):
            # enter the review_url to crawl reviews
            yield Request(url=reviews[i], meta={"douban_id": douban_id}, dont_filter=True, callback=self.review_detailed)

    def review_detailed(self, response):
        review_item = DoubanBookReviewItem()
        douban_id = response.meta["douban_id"]

        review_content = []
        reviews = response.css('.review-content::text').extract()
        for review in reviews:
            content = review.replace('\u3000', '').replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\xa0', '').strip()
            review_content.append(content)

        item_loader = ItemLoader(item=DoubanBookReviewItem(), response=response)
        item_loader.add_value("review", review_content)
        item_loader.add_value("douban_id", douban_id)

        review_item = item_loader.load_item()

        yield review_item
