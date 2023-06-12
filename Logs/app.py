from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import boto3
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/": {"origins": ""}})


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, Bearer"
    return response

@app.route('/logs/guardar_info', methods=['POST'])
def guardar_log():
    texto = request.form.get('texto')
    if texto:
        with open('log.txt', 'a') as archivo_log:
            archivo_log.write(texto + '\n')
        return 'Texto guardado en el log correctamente.'
    else:
        return 'No se proporcionó ningún texto.'

if __name__ == '__main__':
    app.run(debug=True,port=4001)
