from typing import Any

from pymysql.connections import Connection

__all__ = [
    "insertNewPost",
    "insertNewClient",
]
        

def insertNewPost(connection: Connection, post: dict[str, Any]):
    if post:
        name = post['name']
        preview = post['preview']
        text_message = post['text_message']
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT  `web-site`.`posts` (name, preview, text_message) VALUES (%s, %s, %s)", (name, preview, text_message))
            connection.commit()
            cursor.close()
    except Exception as e:
        print(e)
     
        
def insertNewClient(connection, name, login, password):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as `count` FROM `clients` WHERE login LIKE %s", (login))
            res = cursor.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            
    
            cursor.execute("INSERT `clients`\
                (name, login, password) \
                    VALUES (%s, %s, %s)",
                    (name,login,password))
            connection.commit()
            cursor.close() 
            
        return True
    except Exception as e:
        print(e)
        return False