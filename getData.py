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

    def getdetailbuku(self, idbuku):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM buku WHERE idbuku={}".format(idbuku))
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
            "SELECT sedang_pinjam.idsedang_pinjam, sedang_pinjam.tanggal_pinjam, "
            "sedang_pinjam.tanggal_kembali, sedang_pinjam.progress_baca, "
            "buku.idbuku, buku.judul_buku, buku.jumlah_halaman, buku.foto_buku, buku.pengarang, buku.file_buku "
            "FROM (sedang_pinjam INNER JOIN buku ON sedang_pinjam.buku_idbuku = buku.idbuku) "
            "WHERE user_iduser={}".format(iduser))
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result

    def getdatasedangpinjam(self, idpinjam):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sedang_pinjam WHERE idsedang_pinjam = {}".format(idpinjam))
        result = cursor.fetchall()
        cursor.close()
        return result

    def getdatabarupinjam(self, iduser, idbuku):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT idsedang_pinjam FROM sedang_pinjam WHERE user_iduser = {} AND buku_idbuku = {}".format(iduser, idbuku))
        result = cursor.fetchall()
        cursor.close()
        return result[0]['idsedang_pinjam']

    def getdatahistory(self, iduser):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(
            "SELECT riwayat_pinjam.idriwayat_pinjam, riwayat_pinjam.tanggal_pinjam, "
            "riwayat_pinjam.tanggal_dikembalikan, riwayat_pinjam.progress_baca, buku.idbuku, "
            "buku.judul_buku, buku.foto_buku, buku.pengarang "
            "FROM (riwayat_pinjam INNER JOIN buku ON riwayat_pinjam.buku_idbuku = buku.idbuku) "
            "WHERE user_iduser={}".format(iduser))
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result

    def getdatawishlist(self, iduser):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(
            "SELECT * "
            "FROM (daftar_bacaan INNER JOIN buku ON daftar_bacaan.buku_idbuku = buku.idbuku) "
            "WHERE user_iduser={}".format(iduser))
        result = cursor.fetchall()
        cursor.close()
        print(result)
        return result

    def getSearchJudul(self, keyword):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM buku WHERE judul_buku LIKE '%{}%'".format(keyword))
        result = cursor.fetchall()
        cursor.close()
        return result

    def getKategori(self, category):
        mydb = connectdb()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM buku WHERE kategori LIKE '%{}%'".format(category))
        result = cursor.fetchall()
        cursor.close()
        return result

    def listKategori(self):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("SELECT kategori FROM buku")
        result = cursor.fetchall()
        cursor.close()

        catlist = set()

        for r in result:
            li = r[0].split(', ')
            for cat in li:
                catlist.add(cat)

        return list(catlist)



