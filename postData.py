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
    def uploadBuku(self, bookDetails, cover, file):
        judul = bookDetails['judul']
        isbn = bookDetails['isbn']
        pengarang = bookDetails['pengarang']
        penerbit = bookDetails['penerbit']
        tahun = bookDetails['tahun']
        halaman = bookDetails['halaman']
        sinopsis = bookDetails['sinopsis']
        copy = bookDetails['jumlahcopy']
        kategori = bookDetails['kategori']

        mydb = connectdb()
        cur = mydb.cursor()
        cur.execute(
            "INSERT INTO buku (idbuku, judul_buku, isbn, pengarang, penerbit, tahun_terbit, jumlah_halaman, sinopsis, foto_buku, kategori, file_buku, jumlah_copy, total_dipinjam) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (0, judul, isbn, pengarang, penerbit, int(tahun), int(halaman), sinopsis, cover, kategori, file, int(copy),
             0))
        mydb.commit()
        cur.close()

    def uploadUser(self, userdata, foto):
        username = userdata['username']
        password = userdata['password']
        nama = userdata['nama']
        fakultas = userdata['fakultas']
        jurusan = userdata['jurusan']
        angkatan = userdata['angkatan']
        status = userdata['status']

        mydb = connectdb()
        cur = mydb.cursor()
        cur.execute(
            "INSERT INTO user (iduser, username, password, nama_lengkap, foto_user, fakultas, jurusan, angkatan, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (0, username, password, nama, foto, fakultas, jurusan, int(angkatan), status))
        mydb.commit()
        cur.close()


    def postDataPinjam(self, details):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO sedang_pinjam (idsedang_pinjam, tanggal_pinjam, tanggal_kembali, progress_baca, user_iduser, buku_idbuku) VALUES (%s, %s, %s, %s, %s, %s)",
            (0, datetime.fromtimestamp(int(details['tanggalpinjam'])), datetime.fromtimestamp(int(details['tanggalkembali'])), 0, details['iduser'], details['idbuku']))
        mydb.commit()
        cursor.close()

    def postHistory(self, details, sedangpinjam):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO riwayat_pinjam (idriwayat_pinjam, tanggal_pinjam, tanggal_dikembalikan, progress_baca, user_iduser, buku_idbuku) VALUES (%s, %s, %s, %s, %s, %s)",
            (0, sedangpinjam['tanggal_pinjam'], datetime.fromtimestamp(int(details['tanggaldikembalikan'])), sedangpinjam['progress_baca'], int(details['iduser']), int(details['idbuku'])))
        mydb.commit()
        cursor.close()

    def dropSedangpinjam(self, details):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM sedang_pinjam WHERE idsedang_pinjam = {}".format(details))
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

    def updateDikembalikan(self, idbuku):
        mydb = connectdb()
        cursor = mydb.cursor()
        cursor.execute("UPDATE buku SET total_dipinjam = total_dipinjam-1 WHERE idbuku = {}".format(idbuku))
        mydb.commit()
        cursor.close()

