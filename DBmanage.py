import pymysql
from error import *


def get_connection():
    conn = pymysql.connect(host='127.0.0.1', db='auth', user='root', password='password', charset='utf8')

    return conn


def find_user(index=None, email=None, name=None):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    result = None

    if index is not None:
        sql = 'select * from user where index=%s'
        cursor.execute(sql, [index])
        result = cursor.fetchone()

    elif email is not None:
        sql = 'select * from user where email=%s'
        cursor.execute(sql, [email])
        result = cursor.fetchone()

    elif name is not None:
        sql = 'select * from user where name=%s'
        cursor.execute(sql, [name])
        result = cursor.fetchall()

    if result is None:
        cursor.close()
        conn.close()

        raise no_user

    conn.commit()

    cursor.close()
    conn.close()

    return result


def register(email, pw, name):
    try:
        usr = find_user(email=email)

        raise duplicate_user

    except Exception as e:
        if e is no_user:
            pass

        else:
            raise disable

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = 'insert into user(email, hashed_pw, name) values({email}, {hashed_pw}, {name})'\
        .format(email=email, hashed_pw=pw, name=name)
    cursor.execute(sql)
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        conn.close()

        raise disable

    conn.commit()

    cursor.close()
    conn.close()


def login(email=None, pw=None):
    usr = find_user(email=email)

    if pw != usr['hashed_pw']:
        raise no_user

    return