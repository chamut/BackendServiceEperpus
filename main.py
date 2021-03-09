import os
from datetime import datetime

from flask import Flask, request, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from getData import GetData
from login import login
from postData import postData

app = Flask(__name__)
CORS(app)

COVER_FOLDER = "/var/www/html/rr/bookcover/"
FILE_FOLDER = "/var/www/html/rr/bookfile/"
PROFIL_FOLDER = "/var/www/html/rr/userphoto"
now = datetime.now().time()

@app.route("/inputBuku", methods=['POST', 'GET'])
def formBuku():
    if request.method == 'POST':
        bookDetails = request.form
        foto = request.files['cover']
        filename = secure_filename(str(now) + foto.filename)
        foto.save(os.path.join(COVER_FOLDER, filename))
        foto = "http://192.168.1.17/rr/bookcover/" + filename
        file = request.files['filebuku']
        filename = secure_filename(str(now) + file.filename)
        file.save(os.path.join(FILE_FOLDER, filename))
        file = "http://192.168.1.17/rr/bookfile/" + filename
        postData().uploadBuku(bookDetails, foto, file)

    return render_template('formBuku.html')

@app.route("/inputUser", methods=['POST', 'GET'])
def formUser():
    if request.method == 'POST':
        userdata = request.form
        foto = request.files['fotoprofil']
        filename = secure_filename(str(now) + foto.filename)
        foto.save(os.path.join(PROFIL_FOLDER, filename))
        foto = "http://192.168.1.17/rr/userphoto/" + filename
        postData().uploadUser(userdata, foto)

    return render_template('formUser.html')


@app.route("/buku", methods=['GET'])
def dataBuku():
    respon = GetData().getdatabuku()
    respon = {"data" : respon}
    return respon

@app.route("/detailbuku/<idbuku>", methods=['GET'])
def detailBuku(idbuku):
    respon = GetData().getdetailbuku(idbuku)
    respon = {"data" : respon}
    return respon

@app.route("/search/<keyword>")
def dataSearch(keyword):
    respon = GetData().getSearchJudul(keyword)
    if respon != []:
        message = "1"
        respon = {"message": message, "data": respon}
    else:
        message = "0"
        respon = {"message" : message, "data" : respon}
    return respon

@app.route("/kategori/<kategori>")
def dataKategori(kategori):
    respon = GetData().getKategori(kategori)
    respon = {"data" : respon}
    return respon

@app.route("/user", methods=['GET'])
def dataUser():
    respon = GetData().getdatauser()
    respon = {"data" : respon}
    return respon

@app.route("/sedangpinjam/<iduser>", methods=['GET'])
def dataPinjam(iduser):
    user = request.view_args['iduser']
    respon = GetData().getdatapinjambuku(user)
    respon = {"data": respon}
    return respon

@app.route('/pinjam/<iduser>/<idbuku>/<tanggalpinjam>/<tanggalkembali>')
def postPinjam(iduser, idbuku, tanggalpinjam, tanggalkembali):
    try:
        data = request.view_args
        print(data)
        postData().postDataPinjam(details=data)
        postData().updateDipinjam(data['idbuku'])
        idpinjam = GetData().getdatabarupinjam(iduser, idbuku)
        result = {"message": "1", "idpinjam": idpinjam}
    except:
        result = {"message": "0"}

    return result


@app.route('/riwayat/<iduser>/<idbuku>/<idpinjam>/<tanggaldikembalikan>')
def postRiwayat(iduser, idbuku, idpinjam, tanggaldikembalikan):
    try:
        data = request.view_args
        sedangpinjam = GetData().getdatasedangpinjam(idpinjam)
        postData().postHistory(data, sedangpinjam[0])
        postData().dropSedangpinjam(idpinjam)
        postData().updateDikembalikan(idbuku)
        result = {"message" : "1"}
    except:
        result = {"message" : "0"}

    return result

@app.route("/history/<iduser>", methods=['GET'])
def dataHistory(iduser):
    user = request.view_args['iduser']
    respon = GetData().getdatahistory(user)
    respon = {"data": respon}
    return respon

@app.route('/addwishlist/<iduser>/<idbuku>')
def postWishlist(iduser, idbuku):
    try:
        data = request.view_args
        postData().postWishlist(data)
        result = {"message": "1"}
    except:
        result = {"message": "0"}

    return result

@app.route('/removewishlist/<iduser>/<idbuku>')
def removeWishlist(iduser, idbuku):
    try:
        postData().deletewishlist(iduser, idbuku)
        result = {"message": "1"}
    except:
        result = {"message": "0"}

    return result

@app.route('/getwishlist/<iduser>')
def getWishlist(iduser):
    data = request.view_args['iduser']
    respon = GetData().getdatawishlist(data)
    respon = {"data": respon}
    return respon

@app.route('/login/<uname>/<password>')
def isUserin(uname, password):
    respon = login().ceklogin(uname, password)
    if respon != None:
        sukses = "Login Successful"
        respon = {"message": sukses, "data": respon[0]}
    else:
        sukses = "Login Failed"
        respon = {"message": sukses, "data": respon}
    return respon

@app.route('/updatebaca/<idpinjam>/<progress>')
def updateProgress(idpinjam, progress):
    respon = postData().updateProgressBaca(idpinjam=idpinjam, progress=progress)
    result = {"message": respon}

    return result

@app.route("/listkategori")
def getlistCat():
    respon = GetData().listKategori()
    respon = {"data" : respon}
    return respon


"""@app.route("/data/<section>/<apa>")
def data2(section, apa):
    print(int(request.view_args['apa']))
    print(request.view_args['section'])
    return request.view_args['section']"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1298, debug=True)