from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="scrapy_mysql", charset="utf8")
cursor = conn.cursor()


def data_process():
    query_sql = """
                select review_id, review_content 
    """
    cursor.execute(query_sql)
    results = cursor.fetchall()
    for result in results:
        if len(result[1]) <= 30:
            delete_review(result[0])
        else:
            result[1].replace('\n', '').replace('\t', '').replace('\xa0', '').strip()
            update_review(result[0], result[1])


def delete_review():
    delete_sql = """
                DELETE FROM book_reviews WHERE review_content = ','
    """
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


def uniq():
    # SELECT distinct douban_id, title, author, publishing_house, rating, tag, description, rec_book FROM book
    uniq_sql = """
              DELETE FROM book WHERE id NOT IN (
                SELECT id FROM (
                  SELECT MIN(id) AS id FROM book GROUP BY douban_id
                ) AS tmp
              )
    """
    cursor.execute(uniq_sql)

    # results = cursor.fetchall()
    # for result in results:
    #     insert_sql = """
    #                INSERT INTO book_a(douban_id, title, author, publishing_house, rating, tag, description, rec_book)
    #                VALUES (%d, %s, %s, %s, %s, %s, %s, %s)
    #     """ % (result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
    #     try:
    #         # 执行sql语句]
    #         cursor.execute(insert_sql)
    #         # 提交到数据库执行
    #         conn.commit()
    #     except:
    #         # Rollback in case there is any error
    #         conn.rollback()

    conn.close()


def url():
    sql = """
            SELECT douban_id FROM book 
    """
    cursor.execute(sql)

    results = cursor.fetchall()
    for result in results:
        url = "https://book.douban.com/subject/" + result[0] + "/"
        upd_sql = """
                    UPDATE book SET url = %s WHERE douban_id = %s
        """ % (url, result[0])
        try:
            # 执行sql语句
            cursor.execute(upd_sql)
            # 提交到数据库执行
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()

    conn.close()


def count():
    sql = """
        SELECT DISTINCT review_content FROM book_review
    """
    cursor.execute(sql)

    result = cursor.fetchall()
    print(result)

    conn.close()


def insert():
    sql = """
        SELECT DISTINCT review_content, douban_id FROM book_reviews
    """
    cursor.execute(sql)

    select_results = cursor.fetchall()

    for select_result in select_results:
        ins_sql = """
                insert into book_reviews_content(review_content, douban_id)
                VALUES (%s, %s)
        """

        try:
            # 执行sql语句
            cursor.execute(ins_sql, (select_result[0], select_result[1]))
            # 提交到数据库执行
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()

    conn.close()


if __name__ == "__main__":
    insert()
