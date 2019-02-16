import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="scrapy_mysql", charset="utf8")
cursor = conn.cursor()

def crwal_ips():
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"}
    re = requests.get("https://www.xicidaili.com/nn/", headers=headers)

    selector = Selector(text=re.text)
    all_attrs = selector.css("#ip_list tr")

    for attrs in all_attrs:
        speed_str = attrs.css(".bar::attr(title)").extract()
        if speed_str:
            speed = float(speed_str.split("秒")[0])

        attr = attrs.css("td::text").extract()

        ip = attr[0]
        port = attr[1]
        proxy_type = attr[5]
