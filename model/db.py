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

def createDB():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `web-site`")
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

def getUser( user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `clients` WHERE id = {user_id} LIMIT 1")
            res = cursor.fetchall()[0]
            cursor.close()
        if not res:
            print("Пользователь не найден")
            return False
        return res
    except Exception as e:
        print("Ошибка в получении данных из БД " + str(e))

    return False
