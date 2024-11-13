
class FDatabase:
    def __init__(self, db) -> None:
        self._db = db
        self._cursor = db.cursor()
    
