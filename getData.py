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


class GetData:
    def getdatabuku(self):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM buku")
        result = cursor.fetchall()
        cursor.close()
        return result

    def getdatauser(self):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        cursor.close()
        return result

    def getdatapinjambuku(self, iduser):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(
            "SELECT sedang_pinjam.tanggal_pinjam, "
            "sedang_pinjam.tanggal_kembali, sedang_pinjam.progress_baca, "
            "buku.judul_buku, buku.foto_buku, buku.pengarang, buku.file_buku "
            "FROM (sedang_pinjam INNER JOIN buku ON sedang_pinjam.buku_idbuku = buku.idbuku) "
            "WHERE user_iduser={}".format(iduser))
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result
