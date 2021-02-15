from flask import Flask, request
from flask_cors import CORS
from getData import GetData
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

@app.route('/riwayat/<iduser>/<idbuku>/<tanggalpinjam>/<tanggalkembali>')
def postRiwayat(idpinjam, iduser, idbuku, tanggalpinjam, tanggaldikembalikan, progress):
    data = request.view_args
    postData.postHistory(data)
    postData.dropSedangpinjam(data['idpinjam'])


@app.route("/data/<section>/<apa>")
def data2(section, apa):
    print(int(request.view_args['apa']))
    print(request.view_args['section'])
    return request.view_args['section']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1298, debug=True)
