import requests
from scrapy.selector import Selector
import MySQLdb

# 根据豆瓣id爬取某本书的数据
# @INPUT：douban_id
# @OUTPUT: 表示图书信息的json，包括：
# douban_id,title,author,publishing_house,rating
# tag, description, rec_book,review_tag,review_content


def crawlABook(douban_id):
    # TODO
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="xici_ip", charset="utf8")
    cursor = conn.cursor()

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

    url = "https://book.douban.com/subject/" + douban_id + "/"
    re = requests.get(url, headers=headers)

    selector = Selector(text=re.text)
    # link = selector.css('#wrapper h1 span::text').extract()
    title = selector.css('#wrapper h1 span::text').extract()[0]
    rating = selector.css('.rating_self strong::text').extract()[0].strip()
    tag = selector.css('.indent span .tag::text').extract()
    description = selector.css('.related_info .intro p::text').extract()[0:2]
    rec_books = selector.css('#db-rec-section .content dl dd a::text').extract()
    rec_book_list = []
    for rec_book in rec_books:
        rec_book_list.append(rec_book.replace('\n', '').strip())

    review_url = selector.css('.review-list .review-item h2 a::attr(href)').extract()
    review_content = []
    for i in range(0, 10):
        review = requests.get(review_url[i], headers=headers)
        review_selector = Selector(text=review.text)
        reviews = review_selector.css('.review-content::text').extract()
        new_review = []
        for review in reviews:
            content = review.replace('\n', '').replace('\t', '').replace('\xa0', '').strip()
            if content != '':
                new_review.append(content)
        if new_review:
            review_content.append(new_review)

    book = {'id': douban_id, 'title': title, 'rating': rating, 'tag': tag, 'description': description,
            'rec_book_list': rec_book_list, 'review_content': review_content}

    print(book)
    # return book


if __name__ == "__main__":
    crawlABook("4913064")

