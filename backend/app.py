# Librerias empleadas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from flask import (
    Flask, 
    render_template, 
    request,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
from datetime import datetime
import sys
import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/maintenancelocalsocadb'
app.config['UPLOAD_FOLDER'] = ''
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configuración del servidor y las credenciales
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'aldo.jaimes@utec.edu.pe'
smtp_password = 'mmqd rgig sapg nmcb'

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer(), nullable=True)

    def __init__(self, name, lastname, user_name, password, email, phone_number):
        self.name = name
        self.lastname = lastname
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return '<User %r>' % (self.user_name)
    
class traindata(db.Model):
    __tablename__ = 'traindata'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    v1 = db.Column(db.Integer(), nullable=False)
    v2 = db.Column(db.Integer(), nullable=False)
    v3 = db.Column(db.Integer(), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    modifited_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, v1, v2, v3, result):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.result = result

    def __repr__(self):
        return '<Register %r>' % (self.id)

# End Models --------------------------------------------------
    
with app.app_context():
    db.create_all()

# Endpoints

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculadora', methods=['GET'])
def calculadora():
    return render_template('calculadora.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        v1 = int(request.form['v1'])
        v2 = int(request.form['v2'])
        v3 = int(request.form['v3'])
        recomendaciones = []
        if v1 > 120:
            if (v1/v3 < v2*2 and v2 > 0) or (v1/v3 > 2 and v2 == 0):
                recomendaciones.append('Existen posibilidades de que usted padezca de FOMO')
        else:
            recomendaciones.append('No se detectaron problemas')
        return render_template('resultados.html', recomendaciones = recomendaciones)
    except Exception as e:
        print(e)
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error in the calculation'}), 500
    finally:
        db.session.close()

@app.route('/Alogin', methods=['GET'])
def Alogin():
    return render_template('Alogin.html')

@app.route('/Blogin', methods=['GET'])
def Blogin():
    return render_template('Blogin.html')

@app.route('/Aregister', methods=['GET'])
def Aregister():
    return jsonify({'success': True, 'message': 'Registro correcto!'}), 200

@app.route('/Bregister', methods=['POST'])
def Bregister():
    try:
        print("0")
        token = request.form['Token']
        print("1")
        rtoken = request.form['realToken']
        print("2")
        if token == rtoken:
            return jsonify({'success': True, 'message': 'Registro correcto!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Token incorrecto'}), 401
    except Exception as e:
        print(e)
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error in the registration'}), 500

@app.route('/Token', methods=['POST'])
def token():
    try:
        email = request.form['email']
        if email:
            from_email = 'aldo.jaimes@utec.edu.pe'
            to_email = email
            subject = "Token de acceso: SoCa"
            token = "1234"
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
            return render_template('Blogin.html', token=token)
        else:
            return jsonify({'success': False, 'message': 'You need a email'}), 401
    except Exception as e:
        print(e)
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error in the generation of the token'}), 500
    finally:
        db.session.close()

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))

# End of file