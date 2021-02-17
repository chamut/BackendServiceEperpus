from flask import Flask, request
from flask_cors import CORS
from getData import GetData
from login import login
from postData import postData

app = Flask(__name__)
CORS(app)

@app.route("/buku", methods=['GET'])
def dataBuku():
    respon = GetData().getdatabuku()
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
    data = request.view_args
    print(data)
    postData().postDataPinjam(details=data)
    postData().updateDipinjam(data['idbuku'])

@app.route('/riwayat/<iduser>/<idbuku>/<tanggalpinjam>/<tanggalkembali>')
def postRiwayat(idpinjam, iduser, idbuku, tanggalpinjam, tanggaldikembalikan, progress):
    data = request.view_args
    postData().postHistory(data)
    postData().dropSedangpinjam(data['idpinjam'])

@app.route('/addwishlist/<iduser>/<idbuku>')
def postWishlist(iduser, idbuku):
    data = request.view_args
    postData().postWishlist(data)

@app.route('/removewishlist/<idwishlist>')
def removeWishlist(idwishlist):
    data = request.view_args['idwishlist']
    postData().deletewishlist(data)

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

"""@app.route("/data/<section>/<apa>")
def data2(section, apa):
    print(int(request.view_args['apa']))
    print(request.view_args['section'])
    return request.view_args['section']"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1298, debug=True)
