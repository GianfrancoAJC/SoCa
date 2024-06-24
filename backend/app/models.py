from flask_sqlalchemy import SQLAlchemy
from config.local import config
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys


db = SQLAlchemy()

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = config['DATABASE_URI'] if database_path is None else database_path
    db.app = app
    db.init_app(app)
    db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(400), nullable=False)
    chats = db.relationship('Chat', backref='user', lazy=True)
    data = db.relationship('Data', backref='user', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True)

    @property
    def password(self):
        raise AttributeError('Password is not readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return 'User: {}, {}'.format(self.id, self.username)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.created_at = datetime.now()

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            user_created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        
        return user_created_id
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return 'Chat: {}, {}'.format(self.id, self.chat_name)
    
    def __init__(self, user_id, chat_name):
        self.user_id = user_id
        self.chat_name = chat_name
        self.created_at = datetime.now()

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'chat_name': self.chat_name
        }
    
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    message = db.Column(db.String(400), nullable=False)
    chat_id = db.Column(db.String(36), db.ForeignKey('chats.id'), nullable=False)
    sender_type = db.Column(db.String(10), nullable=False)  # 'user' o 'auto'
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    modified_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return 'Message: {}, {}, {}'.format(self.id, self.message, self.sender_type)

    def __init__(self, chat_id, message, sender_type):
        self.chat_id = chat_id
        self.message = message
        self.sender_type = sender_type
        self.created_at = datetime.now()

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'message': self.message,
            'sender_type': self.sender_type,
        }
    
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    r_mean = db.Column(db.Integer(), nullable=False)
    s_mean = db.Column(db.Integer(), nullable=False)
    n_open = db.Column(db.Integer(), nullable=False)
    mt_response = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    modifited_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, user_id, r_mean, s_mean, n_open, mt_response):
        self.user_id = user_id
        self.r_mean = r_mean
        self.s_mean = s_mean
        self.n_open = n_open
        self.mt_response = mt_response
        self.created_at = datetime.now()

    def __repr__(self):
        return '<Register %r>' % (self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'r_mean': self.r_mean,
            's_mean': self.s_mean,
            'n_open': self.n_open,
            'mt_response': self.mt_response,
        }
    