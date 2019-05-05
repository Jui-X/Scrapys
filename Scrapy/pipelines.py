# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline


class ScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class ProductImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "img_url" in item:
            for ok, value in item:
                img_path = value["path"]
            item["img_path"] = img_path

        return item


class CarMysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # item['review'].replace('\n', '').replace('\t', '').replace('\xa0', '').strip()
        # str_rate = ''.join(item['rating'])
        # rate = float(str_rate)
        # if(rate >= 7.5):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # insert_sql = """
        #             insert into book_all(douban_id, title, author, publishing_house)
        #             VALUES (%s, %s, %s, %s)
        #         """
        # cursor.execute(insert_sql, (item["douban_id"], item["title"], item["author"], item["publishing_house"]))
        # insert_sql = """
        #     insert into book(douban_id, title, author, publishing_house, rating, tag, description, rec_book)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        # """
        # cursor.execute(insert_sql, (item["douban_id"], item["title"], item["author"], item["publishing_house"],
        #                             item['rating'], item['tag'], item['description'], item['rec_book']))
        insert_sql = """
                    insert into book_review(douban_id, review_content)
                    VALUES (%s, %s)
                """
        cursor.execute(insert_sql, (item["douban_id"], item["review"]))
