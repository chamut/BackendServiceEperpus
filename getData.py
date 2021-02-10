import mysql.connector

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eperpus_db"
        )

class GetData:
    def getdatabuku(self):
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM buku")
        result = cursor.fetchall()
        return result

    def getdatauser(self):
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        return result

