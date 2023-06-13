from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import boto3
import uuid
import threading
import time
import datetime
import random


app = Flask(__name__)
# CORS(app, resources={r"/": {"origins": ""}})


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, Bearer"
    return response





@app.route('/repartidor/estado_pedido', methods=['POST'])
def estado_pedido():
    orden_id = request.form.get('orden_id')
    if orden_id:
        now = datetime.datetime.now()
        fecha_tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
        lista = ['Orden en proceso', 'Orden entregada', 'Orden en proceso', 'Orden entregada', 'Orden en proceso']
        elemento = random.choice(lista)


        response_log = requests.post('http://localhost:4004/ESB/guardar_info', data={
            'texto': fecha_tiempo + ' - /repartidor/estado_pedido: ' + 'orden_id: ' + orden_id + ' - ' + elemento 
        })
        
        response = jsonify({'message': elemento, 'status': 200})
        response.status_code = 200
        return response
    
@app.route('/repartidor/recibir_pedido', methods=['POST'])
def guardar_log():
    _json = request.form
    orden_id = _json['orden_id']
    
    if orden_id:
        now = datetime.datetime.now()
        fecha_tiempo = now.strftime("%Y-%m-%d %H:%M:%S")

        response_log = requests.post(
            'http://localhost:4004/ESB/guardar_info', 
            data = {
                'texto': fecha_tiempo + ' - /repartidor/recibir_pedido: ' + orden_id
            })
        
        t = threading.Thread(target=temporizador, args=(0.1,orden_id,))
        t.start()
        response = jsonify({'message': 'Pedido recibido por parte repartidor', 'status': 200})
        response.status_code = 200
        return response
    else:
        response = jsonify({'message': 'No se proporcionó un pedido', 'status': 400})
        response.status_code = 400
        return response
    

def temporizador(tiempo_en_minutos,orden_id):
    tiempo_en_segundos = tiempo_en_minutos * 60
    time.sleep(tiempo_en_segundos)
    now = datetime.datetime.now()
    fecha_tiempo = now.strftime("%Y-%m-%d %H:%M:%S")

    response_log = requests.post(
        'http://localhost:4004/ESB/guardar_info',
         data = {
             'texto': fecha_tiempo + ' - repartidor -> orden_id:' + orden_id + ' pedido entregado con exito'
         } 
         )
    print("¡El temporizador ha terminado!")
if __name__ == '__main__':
    app.run(debug=True,port=4002)
