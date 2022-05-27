import sqlite3, logging

class ValidatorCache:
    def __init__(self, dbpath:str):
        self.db = sqlite3.connect(dbpath)
        try:
            self.createTable()
        except sqlite3.OperationalError as ex:
            pass
        
    def createTable(self):
        self.db.execute('''CREATE TABLE validatorCache
        (approach TEXT NOT NULL,
        subject TEXT NOT NULL,
        predicate TEXT NOT NULL,
        object TEXT NOT NULL,
        score REAL NOT NULL);''')
        
    def close(self):
        self.db.close()
        
    def insert(self, approach:str, sub:str, pred:str, obj:str, score:float):
        temp = [(approach), (sub), (pred), (obj), (score)]
        self.db.execute("INSERT INTO validatorCache (approach, subject, predicate, object, score) VALUES (?, ?, ?, ?, ?)", temp)
        self.db.commit()
    
    def getScore(self, approach:str, sub:str, pred:str, obj:str):
        input = [(approach), (sub), (pred), (obj)]
        cursor = self.db.execute('SELECT score FROM validatorCache WHERE approach=? AND subject=? AND predicate=? AND object=?', input)
        for row in cursor:
            return row[0]