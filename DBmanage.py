import pymysql


def get_connection():
    conn = pymysql.connect(host='127.0.0.1', db='auth', user='root', password='password', charset='utf8')

    return conn


def func():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = ''
    cursor.execute(sql)
    result = cursor.fetchall()

    conn.commit()

    cursor.close()
    conn.close()