# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from testScrapy.items import DoubanBookItem
from scrapy.loader import ItemLoader


class DoubanSpider(scrapy.Spider):
    name = 'douban_book'
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
            yield Request(url=post_url, meta={"book_info": book_info}, dont_filter=True, callback=self.parse_detailed)

        # 获取下一页url并继续交给scrapy下载
        #next_url = response.css('.next a::attr(href)').extract_first("")
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse())

    def parse_detailed(self, response):
        # 提取文章详情页的具体字段：书名 作者 出版社 关键词 分类 评分 喜欢这本书的人还喜欢什么
        book_item = DoubanBookItem()
        rec_book_list = []

        book_info = response.meta["book_info"]

        book = book_info[0].replace('\n', '').strip().split('/')
        authors = book[0]
        publishing_house = book[-3]

        # title = response.css('#wrapper h1 span::text').extract()[0]
        # rating = response.css('.rating_self strong::text').extract()[0].strip()
        # tag = response.css('.indent span .tag::text').extract()
        ISBN = response.css("#info::text").extract()[-2].replace(" ", '')
        rec_books = response.css('#db-rec-section .content dl dd a::text').extract()
        for rec_book in rec_books:
            rec_book.replace('\n', '').strip()
            rec_book_list.append(rec_book.replace('\n', '').strip())

        item_loader = ItemLoader(item=DoubanBookItem(), response=response)
        item_loader.add_value("ISBN", ISBN)
        item_loader.add_css("title", "#wrapper h1 span::text")
        item_loader.add_value("author", authors)
        item_loader.add_value("publishing_house", publishing_house)
        item_loader.add_css("rating", ".rating_self strong::text")
        item_loader.add_css("tag", ".indent span .tag::text")
        item_loader.add_value("rec_book", rec_book_list)

        book_item = item_loader.load_item()

        yield book_item

