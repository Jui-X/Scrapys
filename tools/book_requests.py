import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="xici_ip", charset="utf8")
cursor = conn.cursor()


def crawl_books(douban_id):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

    # re = requests.get("https://book.douban.com/subject_search?search_text=%E6%B4%BB%E7%9D%80&cat=1001")
    url = "https://book.douban.com/subject/" + douban_id + "/"
    re = requests.get(url, headers=headers)

    selector = Selector(text=re.text)
    link = selector.css('#wrapper h1 span::text').extract()
    print(link)


if __name__ == "__main__":
    crawl_books("25862578")