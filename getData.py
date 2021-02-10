import mysql.connector
import yaml

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
mydb = mysql.connector.connect(
            host= db['host'],
            user= db['user'],
            password= db['password'],
            database= db['database']
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

