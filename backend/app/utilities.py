from app.models import db, Message
import random
import time

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración del servidor y las credenciales
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'aldo.jaimes@utec.edu.pe'
smtp_password = 'mmqd rgig sapg nmcb'