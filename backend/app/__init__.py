from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from .models import db, setup_db, Chat, Message, Data
from flask_cors import CORS
from .utilities import allowed_file
from .users_controller import users_bp
from .authentication import authorize
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Configuración del servidor y las credenciales
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'aldo.jaimes@utec.edu.pe'
smtp_password = 'mmqd rgig sapg nmcb'

def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        app.config['UPLOAD_FOLDER'] = ''
        app.register_blueprint(users_bp)
        setup_db(app, test_config['database_path'] if test_config else None)
        CORS(app, origins=['http://localhost:8080'])

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/chat', methods=['POST'])
    @authorize
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
    @authorize
    def new_chat():
        try:
            data = request.get_json()
            user_id = data['user_id']
            chat_name = data['chat_name']
            chat = Chat(user_id=user_id, chat_name=chat_name)
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
    @authorize
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
    @authorize
    def new_messages():
        try:
            data = request.get_json()
            chat_id = data['chat_id']
            message = data['message']
            new_message = Message(chat_id=chat_id, message=message)
            db.session.add(new_message)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': new_message.serialize()
            }), 201
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Error saving message'
            }), 500
    
    @app.route('/data', methods=['POST'])
    @authorize
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
    @authorize
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