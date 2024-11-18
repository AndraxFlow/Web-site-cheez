
class FDatabase:
    def __init__(self, db) -> None:
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self) -> list:
        sql = """SELECT * FROM `posts`"""
        try:
            self.__cursor.execute(sql)
            res = self.__cursor.fetchall()
            if res:
                return res
        except Exception as e:
            print("Ошибка чтения из БД", e)
        return []
    
    # def getUser(self):
    #     sql = 
    
    def insertNewPost(self, post):
        if post:
            name = post['name']
            preview = post['preview']
            text_message = post['text_message']
            # owner_id = post['owner_id']
        else:
            return
        try:
            self.__cursor.execute("""INSERT  `web_site`.`posts` 
                                  (name, preview, text_message) 
                                  VALUES (%s, %s, %s)""", 
                                  (name, preview, text_message))
            self.__db.commit()
        except Exception as e:
            print("Ошибка в добавлении статьи в БД", e)
            return False
        
        return True
    
    def insertNewClient(self, name, email, password):
        try:
            self.__cursor.execute(f"SELECT COUNT(*) as `count` FROM `clients` WHERE email = {email}")
            res = self.__cursor.fetchall()[0]
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            self.__cursor.execute("INSERT `clients`\
                    (name, email, password) \
                    VALUES (%s, %s, %s)",
                    (name,email,password))
            self.__db.commit()
            self.__cursor.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def getPosts(self):
        try:
            self.__cursor.execute("SELECT *\
                FROM posts\
                ORDER BY created_at;")
            result = self.__cursor.fetchall()
        except Exception as ex:
            result = None
            print(ex)
        return result
        
    def getPost(self, id_post):
        try:
            self.__cursor.execute(f"SELECT * \
                FROM `web_site`.`posts` \
                WHERE id = {id_post};")
            result = self.__cursor.fetchall()[0]
        except Exception as ex:
            result = None
            print(ex)
        return result
    
    def deletePost(self, id_post):
        try:
            self.__cursor.execute(f"DELETE FROM `web_site`.`posts`\
                WHERE (`id` = '{id_post}');")
            self.__db.commit()
            self.__cursor.close()
        except Exception as ex:
            print('ошибка при удалении поста',ex)
    
    def updatePost(self, id_post, name, preview, text_message):
        try:
            if name != '':
                self.__cursor.execute("UPDATE posts\
                    SET name=%s WHERE id = %s;",
                    (name,id_post))
            if preview != '':
                self.__cursor.execute("UPDATE posts\
                    SET preview=%s WHERE id = %s;",
                    (preview,id_post))
            if text_message != '':
                self.__cursor.execute("UPDATE posts\
                    SET text_message=%s WHERE id = %s;",
                    (text_message,id_post))
            self.__db.commit()
        except Exception as e:
            print('Ошибка при обновлении данных поста',e)
    
    
    
    def closeConnect(self):
        self.__cursor.close()