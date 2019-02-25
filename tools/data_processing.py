from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="readme", charset="utf8")
cursor = conn.cursor()


def data_process():
    query_sql = """
                select review_id, review_content from book_review 
    """
    cursor.execute(query_sql)
    results = cursor.fetchall()
    for result in results:
        if len(result[1]) <= 30:
            delete_review(result[0])
        else:
            result[1].replace('\n', '').replace('\t', '').replace('\xa0', '').strip()
            update_review(result[0], result[1])


def delete_review(review_id):
    delete_sql = """
                DELETE FROM book_review WHERE review_id = %d
    """ % review_id
    try:
        # 执行sql语句
        cursor.execute(delete_sql)
        # 提交到数据库执行
        conn.commit()
    except:
        # Rollback in case there is any error
        conn.rollback()


def update_review(review_id, review_content):
    update_sql = """
                UPDATE book_reivew SET review_content = %s WHERE review_id = %d
    """ % (review_id, review_content)
    try:
        # 执行sql语句
        cursor.execute(update_sql)
        # 提交到数据库执行
        conn.commit()
    except:
        # Rollback in case there is any error
        conn.rollback()


if __name__ == "__main__":
    data_process()