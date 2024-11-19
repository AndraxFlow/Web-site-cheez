import pymysql
from pymysql.connections import Connection

from common.config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER


__all__ = [
    "get_connection",
    "createDB",
]

def get_connection() -> Connection:
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        print('not connected', e)


def createDB() -> None:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `web_site`")
            connection.commit()
    except Exception as ex:
        print(ex)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS `clients` (\
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            email text NOT NULL,
                            password text NOT NULL,
                            time integer NOT NULL
                            );"""
                            )
            connection.commit()
    except Exception as ex:
        print(ex)
