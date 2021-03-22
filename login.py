import mysql.connector
import yaml

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)


def connectdb():
    mydb = mysql.connector.connect(
        host=db['host'],
        user=db['user'],
        password=db['password'],
        database=db['database']
    )
    return mydb

class login:
    def ceklogin(self, username, password):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE (username = '{uname}') AND (password = '{pwd}')".format(uname=username, pwd=password[29:]))
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 1:
            return result
        else:
            return None