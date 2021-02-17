from datetime import datetime

import mysql.connector
import yaml

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
def connectdb():
    mydb = mysql.connector.connect(
            host= db['host'],
            user= db['user'],
            password= db['password'],
            database= db['database']
        )
    return mydb

class postData:
    def postDataPinjam(self, details):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO sedang_pinjam (idsedang_pinjam, tanggal_pinjam, tanggal_kembali, progress_baca, user_iduser, buku_idbuku) VALUES (%s, %s, %s, %s, %s, %s)",
            (0, datetime.fromtimestamp(int(details['tanggalpinjam'])), datetime.fromtimestamp(int(details['tanggalkembali'])), 0, details['iduser'], details['idbuku']))
        mydb.commit()
        cursor.close()

    def postHistory(self, details):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO riwayat_pinjam (idriwayat_pinjam, tanggal_pinjam, tanggal_dikembalikan, progress_baca, user_iduser, buku_idbuku) VALUES (%s, %s, %s, %s, %s, %s)",
            (0, datetime.fromtimestamp(details['tanggalpinjam']), datetime.fromtimestamp(details['tanggaldikembalikan']), details['progress'], details['iduser'], details['idbuku']))
        mydb.commit()
        cursor.close()

    def dropSedangpinjam(self, details):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM sedang_pinjam WHERE idsedang_pinjam = {}".format(details['idpinjam']))
        mydb.commit()
        cursor.close()

    def postWishlist(self, details):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO daftar_bacaan (iddaftar_bacaan, user_iduser, buku_idbuku) VALUE (%S, %S,%S)",
                       (0, details['iduser'], details['idbuku']))
        mydb.commit()
        cursor.close()

    def deletewishlist(self, data):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM daftar_bacaan WHERE iddaftar_bacaan = {}".format(data))
        mydb.commit()
        cursor.close()

    def updateDipinjam(self, idbuku):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("UPDATE buku SET total_dipinjam = total_dipinjam+1 WHERE idbuku = {}".format(idbuku))
        mydb.commit()
        cursor.close()

    def updateProgressBaca(self, idpinjam, progress):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("UPDATE sedang_pinjam SET progress_baca = {} WHERE idsedang_pinjam = {}".format(progress, idpinjam))
        mydb.commit()
        cursor.close()

