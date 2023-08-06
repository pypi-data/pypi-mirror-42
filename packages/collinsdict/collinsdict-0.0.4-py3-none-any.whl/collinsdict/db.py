import os
import sqlite3

class DB():
    '''db manage'''
    def __init__(self):
        home = os.path.dirname(__file__)
        self.conn = sqlite3.connect(home+'dict.db')

    def get(self,word):
        result = {}
        try:
            c = self.conn.cursor()
            result ={}
            sql = "SELECT * FROM META WHERE WORD = ?"
            cursor = c.execute(sql,(word,))
            for row in cursor.fetchall():
                result['Word'] = row[0]
                result['Phonetic'] = row[1]
                result['Rank'] = row[2]
                result['Star'] = row[3]
                result['Addition'] = row[4]
            trans = []
            sql = "SELECT * FROM TRANS WHERE WORD = ?"
            cursor = c.execute(sql,(word,))
            for row in cursor:
                trans.append({
                    'Order':row[1],
                    'Major':row[2],
                    'Examples':row[3].split('\n'),
                })
            result['Trans'] = trans
            return result

        except Exception as err:
            if "no such table" in str(err):
                self.createTables()
            print(err)

    def insert(self,word):
        c =self.conn.cursor()
        sql = "INSERT INTO META VALUES (?,?,?,?,?);"
        c.execute(sql,(word['Word'],word['Phonetic'],word['Rank'],word['Star'],word['Addition']))
        sql = "INSERT INTO TRANS VALUES (?,?,?,?);"
        for tran in word['Trans']:
            c.execute(sql,(word['Word'],tran['Order'],tran['Major'],'\n'.join(tran['Examples'])))
        self.conn.commit()

    def createTables(self):
        c = self.conn.cursor()
        try:
            c.execute('''
                DROP TABLE META;
            ''')
            c.execute('''
                DROP TABLE TRANS;
            ''')
        except Exception:
            pass
        c.execute('''
            CREATE TABLE META(
        WORD TEXT PRIMARY KEY NOT NULL,
        PHONETIC TEXT,
        RANK TEXT NOT NULL,
        STAR TEXT NOT NULL,
        ADDITION TEXT
        );
        ''')
        c.execute('''
            CREATE TABLE TRANS(
        WORD TEXT NOT NULL,
        ID TEXT NOT NULL,
        MAJOR TEXT NOT NULL,
        EXAMPLES TEXT,
        PRIMARY KEY (WORD,ID),
        FOREIGN KEY (WORD) REFERENCES META(WORD)
        );
        ''')
        print("Table create success")

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    db=DB()
    # print(db.get("abstain"))
    print(db.get("test"))
