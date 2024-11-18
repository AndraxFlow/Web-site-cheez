
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
        except:
            print("Ошибка чтения из БД абоба")
        return []