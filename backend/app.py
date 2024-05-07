from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ruta para obtener el token de acceso de Facebook
@app.route('/login', methods=['POST'])
def login():
    token = request.json['token']
    # Aquí puedes hacer la validación del token con Facebook y obtener información del usuario si es necesario
    return jsonify({'message': 'Token verificado correctamente'})

# Ruta para enviar un mensaje a través de la API de Facebook
@app.route('/messages', methods=['POST'])
def send_message():
    token = request.headers.get('Authorization')
    message = request.json['message']
    # Aquí puedes enviar el mensaje utilizando la API de Facebook
    return jsonify({'message': 'Mensaje enviado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
