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

def generate_random_response(chat_id):
    responses = [
        "Hola, ¿cómo estás?",
        "¿Qué cuentas?",
        "¡Qué interesante!",
        "¿Podrías decirme más sobre eso?",
        "¡Eso suena genial!",
        "¿Qué planes tienes para hoy?",
        "¿Cómo va todo?",
        "¡Eso es genial!",
        "¿Te gustaría hacer algo más tarde?",
        "¡Qué buena idea!"
    ]
    delay = random.randint(0, 300)
    time.sleep(delay)
    response = random.choice(responses)
    new_message = Message(chat_id=chat_id, message=response, sender_type='auto')
    db.session.add(new_message)
    db.session.commit()
