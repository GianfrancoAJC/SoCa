from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from app.models import db, setup_db, Chat, Message, Data
from flask_cors import CORS
from app.utilities import allowed_file, smtp_server, smtp_port, smtp_user, smtp_password
from app.users_controller import users_bp
from app.authentication import authorize
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from threading import Thread
import requests
import random
import time

def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = ''
        app.register_blueprint(users_bp)
        setup_db(app, test_config['database_path'] if test_config else None)
        CORS(app, origins=["http://localhost:5001", "http://localhost:8081", "*"])

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    def generate_random_response(chat_id, message):
        message = message.lower()
        for i in range(len(message) - 3):
            if message[i:i+4] == 'hola' or message[i:i+4] == 'dias' or message[i:i+4] == 'tard' or message[i:i+4] == 'noch':
                responses = ['Hola, ¿cómo estás?', 'Buenos días, ¿cómo estás?', 'Buenas tardes, ¿cómo estás?', 'Buenas noches, ¿cómo estás?']
                break
            elif message[i:i+4] == 'como' or message[i:i+4] == 'esta':
                responses = ['Estoy bien, gracias por preguntar. ¿Y tú?', 'Estoy bien, ¿y tú?', 'Todo bien, ¿y tú?', 'Todo bien, ¿y tú?']
                break
            elif message[i:i+4] == 'bien' or message[i:i+4] == 'grac':
                responses = ['¿Como va tu día?', '¿Qué tal tu día?', '¿Qué has hecho hoy?', 'Cuentame de tu vida']
                break
            elif message[i:i+4] == 'adios' or message[i:i+4] == 'chao' or message[i:i+4] == 'hast':
                responses = ['Adiós, que tengas un buen día', 'Chao, que tengas un buen día', 'Hasta luego, que tengas un buen día', 'Nos vemos, que tengas un buen día']
                break
            else:
                responses = ['Dejame contarte algo', 'no te imaginas lo que me paso', 'me encanta hablar contigo', 'que opinas de esto']
        response = random.choice(responses)
        delay = random.randint(0, 10)
        time.sleep(delay)
        new_message = Message(chat_id=chat_id, message=response, sender_type='auto')
        db.session.add(new_message)
        db.session.commit()
        amessage = new_message.serialize()
        return amessage
    
    @app.route('/chat', methods=['POST'])
    # @authorize
    def get_user_chats():
        try:
            data = request.get_json()
            user_id = data['user_id']
            chats = Chat.query.filter_by(user_id=user_id).all()
            return jsonify({
                'success': True,
                'chats': [chat.serialize() for chat in chats]
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            return jsonify({
                'success': False,
                'message': 'Error getting user chats'
            }), 500
        
    @app.route('/chats', methods=['POST'])
    # @authorize
    def new_chat():
        try:
            data = request.get_json()
            n = data['n']
            for i in range(n):
                user_id = data['user_id']
                chat_name = data['chats'][i]['name']
                chat_relationship = data['chats'][i]['relationship']
                chat = Chat(user_id=user_id, chat_name=chat_name, chat_relationship=chat_relationship)
                db.session.add(chat)
                db.session.commit()
            return jsonify({
                'success': True,
                'chat': chat.serialize()
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Error saving chat'
            }), 500

    @app.route('/message', methods=['POST'])
    # @authorize
    def get_chat_messages():
        try:
            data = request.get_json()
            chat_id = data['chat_id']
            messages = Message.query.filter_by(chat_id=chat_id).all()
            return jsonify({
                'success': True,
                'messages': [message.serialize() for message in messages]
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            return jsonify({
                'success': False,
                'message': 'Error getting chat messages'
            }), 500
    
    @app.route('/messages', methods=['POST'])
    # @authorize
    def new_messages():
        try:
            data = request.get_json()
            chat_id = data['chat_id']
            message = data['message']
            new_message = Message(chat_id=chat_id, message=message, sender_type='user')
            db.session.add(new_message)
            db.session.commit()
            # Llamada al endpoint de respuesta automática
            amessage = requests.post('http://localhost:5001/auto_response', json={'chat_id': chat_id})
            amessage = amessage.json()["response"]
            return jsonify({
                'success': True,
                'message': new_message.serialize(),
                'amessage': amessage
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Error saving message'
            }), 500
        
    @app.route('/auto_response', methods=['POST'])
    def auto_response():
        try:
            data = request.get_json()
            chat_id = data['chat_id']
            response = generate_random_response(chat_id, Message.query.filter_by(chat_id=chat_id, sender_type = "user").all()[-1].message)
            return jsonify({'success': True, 'message': 'Response will be generated', 'response': response}), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            return jsonify({'success': False, 'message': 'Error generating response'}), 500
    
    @app.route('/data', methods=['POST'])
    # @authorize
    def get_data():
        try:
            data = request.get_json()
            user_id = data['user_id']
            data = Data.query.filter_by(user_id=user_id).all()
            return jsonify({
                'success': True,
                'data': [d.serialize() for d in data]
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            return jsonify({
                'success': False,
                'message': 'Error getting user data'
            }), 500
        
    @app.route('/datas', methods=['POST'])
    # @authorize
    def new_data():
        try:
            data = request.get_json()
            user_id = data['user_id']
            r_mean = data['r_mean']
            s_mean = data['s_mean']
            n_open = data['n_open']
            mt_response = data['mt_response']
            new_data = Data(user_id=user_id, r_mean=r_mean, s_mean=s_mean, n_open=n_open, mt_response=mt_response)
            db.session.add(new_data)
            db.session.commit()
            return jsonify({
                'success': True,
                'data': new_data.serialize()
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Error saving data'
            }), 500
        
    @app.route('/analytics', methods=['POST'])
    def get_analytics():
        try:
            data = request.get_json()
            user_id = data['user_id']
            chats = Chat.query.filter_by(user_id=user_id).all()
            messages = Message.query.filter_by(chat_id=chats[-1].id).all()
            total_messages = 0
            for chat in chats:
                for message in chat.messages:
                    if message.sender_type == 'user':
                        total_messages += 1
            conection_time = messages[-1].created_at - messages[0].created_at if messages else timedelta(0)
            chat_time = 0
            for chat in chats:
                for message in chat.messages:
                    chat_time += len(message.message)/4.14 if message.sender_type == 'user' else 0
            average_chat_time = chat_time / len(chats) if len(chats) > 0 else 0
            average_message_time = chat_time / total_messages if total_messages > 0 else 0
            average_response_time = 0
            for chat in chats:
                for i in range(1, len(chat.messages)):
                    if chat.messages[i].sender_type == 'user':
                        average_response_time += (chat.messages[i].created_at - chat.messages[i-1].created_at).total_seconds()
            average_response_time /= total_messages
            average_await_time = 0
            for chat in chats:
                for i in range(1, len(chat.messages)):
                    if chat.messages[i].sender_type == 'auto':
                        average_await_time += (chat.messages[i].created_at - chat.messages[i-1].created_at).total_seconds()
            average_await_time /= total_messages
            return jsonify({
                'success': True,
                'total_messages': total_messages,
                'conection_time': conection_time.total_seconds(),
                'chat_time': chat_time,
                'average_response_time': average_response_time,
                'average_await_time': average_await_time,
                'average_chat_time': average_chat_time,
                'average_message_time': average_message_time
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            return jsonify({
                'success': False,
                'message': 'Error getting analytics'
            }), 500
        
    @app.route('/Token', methods=['POST'])
    def token():
        try:
            email = request.form['username']
            if email:
                from_email = 'aldo.jaimes@utec.edu.pe'
                to_email = email
                subject = "Token de acceso: SoCa"
                token = int(datetime.now())
                body = f"Su token de acceso es: {token}"
                message = MIMEMultipart()
                message['From'] = from_email
                message['To'] = to_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_email, message.as_string())
                server.quit()
                return jsonify({'success': True, 'message': 'Token enviado!', 'token': token}), 200
            else:
                return jsonify({'success': False, 'message': 'You need a email'}), 401
        except Exception as e:
            print(e)
            print(sys.exc_info())
            return jsonify({'success': False, 'message': 'Error in the generation of the token'}), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal Server error'
        }), 500

    return app