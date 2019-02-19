import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="xici_ip", charset="utf8")
cursor = conn.cursor()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}


def crawl_ips():

    for i in range(30):
        re = requests.get("https://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_attrs = selector.css("#ip_list tr")

        ip_list = []
        for attrs in all_attrs[1:]:
            speed_str = attrs.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])

            attr = attrs.css("td::text").extract()

            ip = attr[0]
            port = attr[1]
            proxy_type = attr[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                """insert into ip_proxy(ip, port, proxy_type, speed) VALUES ('{0}', '{1}', 'HTTP', '{2}')
                """.format(ip_info[0], ip_info[1], ip_info[3])
            )

            conn.commit()


class GetIP(object):
    def get_random_ip(self):
        random_sql = """
                SELECT ip, port FROM ip_proxy
                ORDER BY RAND()
                LIMIT 1
        """
        result = cursor.execute(random_sql)

        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()

    def judge_ip(self, ip ,port):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)

        try:
            proxy_dict = {
                "http": proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status.code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def delete_ip(self, ip):
        delete_sql = """
                    delete from ip_proxy where ip = '{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return  True


if __name__ == "__main__":
    crawl_ips()
    # get_ip = GetIP()
    # get_ip.get_random_ip()