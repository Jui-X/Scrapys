import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="xici_ip", charset="utf8")
cursor = conn.cursor()


def crawl_books(search_text):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

    param = {"search_text": search_text, "cat": "1001"}
    # re = requests.get("https://book.douban.com/subject_search?search_text=%E6%B4%BB%E7%9D%80&cat=1001")
    re = requests.get("https://book.douban.com/subject_search", params=param, headers=headers)

    selector = Selector(text=re.text)
    link = selector.css('#root .item-root a::attr(href)').extract()
    print(link)


if __name__ == "__main__":
    crawl_books(9787506365437)