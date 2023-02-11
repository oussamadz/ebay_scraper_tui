import sqlite3
import datetime


class Connector():

    def __init__(self, ConnectionString):
        self.conn = sqlite3.connect(ConnectionString)
        self.cur = self.conn.cursor()

    def getTasks(self):
        self.cur.execute("SELECT * FROM TASKS;")
        return self.cur.fetchall()

    def getItemCount(self, id):
        self.cur.execute(f"SELECT COUNT(*) FROM ITEMS WHERE id={id};")
        return self.cur.fetchone()[0]

    def addTask(self, taskData):
        now = datetime.datetime.now()
        self.cur.execute(
            f"INSERT INTO TASKS (url, status, notes, lastchecked)"
            f" VALUES ('{taskData[0]}', '{taskData[1]}',"
            f" '{taskData[2]}', '{now}');")
        self.conn.commit()
        taskData.insert(0, self.cur.lastrowid)
        return taskData

    def removeTask(self, id):
        self.cur.execute(f"DELETE FROM TASKS WHERE id = {id};")
        self.conn.commit()

    def getItems(self, taskID):
        self.cur.execute(f"SELECT substr(title,1,50),condition,price,sell,shipping,url FROM ITEMS WHERE hide = 0 AND task = {taskID};")
        return self.cur.fetchall()

    def hideItem(self, id):
        self.cur.execute(f"UPDATE ITEMS SET hide = 1 WHERE id = {id};")
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()
