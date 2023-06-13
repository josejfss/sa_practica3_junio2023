from flask import Flask, request, jsonify
import datetime
import requests

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, Bearer"
    return response



@app.route('/cliente/verificar_orden_repartidor', methods=['POST'])
def verificarRep():
    orden_id = request.form.get('orden_id')
    if orden_id:
        now = datetime.datetime.now()
        fecha_tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
        
        response = requests.post(
            'http://localhost:4004/ESB/estado_pedido_repartidor', 
            data =request.form 
            )
        
        
        json = response.json()
        elemento = json.get('message')

        response_log = requests.post(
            'http://localhost:4004/ESB/guardar_info',
             data = {
                'texto': fecha_tiempo + ' - cliente/verificar_orden_repartidor: ' + 'orden_id: ' + orden_id + ' - ' + elemento 
             }
             )
        
        response = jsonify({'message': elemento, 'status': 200})
        response.status_code = 200
        return response

    else:
        response = jsonify({'message': 'Porfavor ingrese orden_id', 'status': 400})
        response.status_code = 400
        return response



@app.route('/cliente/verificar_orden_restaurante', methods=['POST'])
def verificar():
    _json = request.form
    orden_id = _json['orden_id']


    if orden_id:
        now = datetime.datetime.now()
        fecha_tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
       
        response = requests.post(
            'http://localhost:4004/ESB/estado_pedido_restaurante', 
            data = request.form
            )
        
        json = response.json()

        response_log = requests.post('http://localhost:4004/ESB/guardar_info',
                                     data = {
                                         'texto': fecha_tiempo + ' - cliente/verificarOrdenRes: ' + 'orden_id: ' + orden_id + ' - ' + json.get('message')   
                                     })
        
        response = jsonify({'message': json.get('message') , 'status': 200})
        response.status_code = 200
        return response

    else:
        response = jsonify({'message': 'Porfavor ingrese orden_id', 'status': 400})
        response.status_code = 400
        return response



@app.route('/cliente/solicitar_pedido_r', methods=['POST'])
def solicitar_p():
    _json = request.form
    pedido = _json['pedido']
    direccion = _json['direccion']


    if pedido:
        now = datetime.datetime.now()
        fecha_tiempo = now.strftime("%Y-%m-%d %H:%M:%S")


        response = requests.post(
            'http://localhost:4004/ESB/recibir_pedido_cliente',
            data = {
                'log':  fecha_tiempo + ' - cliente/solicitar_pedido: ' + pedido + '|' + direccion,
                'pedido': pedido,
                'direccion': direccion
                }
        )
        
        
        if response.status_code != 200:
            response = jsonify({'message': 'Se ha enviado el pedido, pero el restaurante aún no ha abierto', 'status': 200})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Pedido recibido por el restaurente', 'status': 200})
            response.status_code = 200
            return response
    else:
        response = jsonify({'message': 'No se proporcionó un pedido o la información es incorrecta', 'status': 400})
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run(debug=True,port=4000)
