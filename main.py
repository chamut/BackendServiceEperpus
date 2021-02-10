from flask import Flask, request
from flask_cors import CORS
from getData import GetData

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1298, debug=True)

