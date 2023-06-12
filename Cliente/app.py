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
        response = requests.post('http://localhost:4002/repartidor/estado_pedido', data=request.form)
        json = response.json()
        elemento = json.get('message')
        form_data = {
            'texto': fecha_tiempo + ' - cliente/verificar_orden_repartidor: ' + 'orden_id: ' + orden_id + ' - ' + elemento 
        }
        response_log = requests.post(
            'http://localhost:4001/logs/guardar_info',
             data = form_data
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
            'http://localhost:4003/restaurante/estado_pedido', 
            data = request.form
            )
        
        json = response.json()
        #elemento = response.json().message
        form_data = {
            'texto': fecha_tiempo + ' - cliente/verificarOrdenRes: ' + 'orden_id: ' + orden_id + ' - ' + json.get('message') 
        }
        response_log = requests.post('http://localhost:4001/logs/guardar_info', data=form_data)
        
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
        form_data = {
            'texto': fecha_tiempo + ' - cliente/solicitar_pedido: ' + pedido + '|' + direccion
        }
        response_log = requests.post(
            'http://localhost:4001/logs/guardar_info', 
            data = form_data
            )
        
        response = requests.post(
            'http://localhost:4003/restaurante/recibir_pedido', 
            data = request.form)
        
        
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
