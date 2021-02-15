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

