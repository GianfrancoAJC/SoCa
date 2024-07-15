from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)
import jwt
import datetime
from app.models import User
from config.local import config

users_bp = Blueprint('/users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    error_lists = []
    returned_code = 201
    try:
        body = request.get_json()

        if 'utoken' not in body:
            error_lists.append('token is required')
            utoken = None
        else:
            utoken = body.get('utoken')

        if 'rtoken' not in body:
            error_lists.append('Server token error')
            rtoken = None
        else:
            rtoken = body.get('rtoken')

        if 'username' not in body:
            error_lists.append('username is required')
            user_db = None
        else:
            username = body.get('username')
            user_db = User.query.filter(User.username == username).first()

        if 'password' not in body:
            error_lists.append('password is required')
            password = "No password provided"
        else:
            password = body.get('password')

        if 'confirmationPassword' not in body:
            error_lists.append('confirmationPassword is required')
            confirmationPassword = "No confirmationPassword provided"
        else:
            confirmationPassword = body.get('confirmationPassword')

        if user_db is not None:
            if user_db.username == username:
                error_lists.append(
                    'An account with this username already exists')
        else:
            if len(password) < 8:
                error_lists.append('Password must have at least 8 characters')

            if password != confirmationPassword:
                error_lists.append(
                    'password and confirmationPassword does not match')
                
            if utoken != rtoken:
                error_lists.append('Wrong token')

        if len(error_lists) > 0:
            returned_code = 400
        else:
            user = User(username=username, password=password)
            user_created_id = user.insert()

            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=1440)
            }, config['SECRET_KEY'], config['ALGORYTHM'])

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error creating a new user'
        }), returned_code
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user_created_id,
        }), returned_code


@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    returned_code = 200   
    try:
        user = User.query.get(user_id) 

        if user is None:
            returned_code = 404
        user.delete()

    except Exception as e:
        print('\te: ', e)
        returned_code = 500

    if returned_code != 200:
        abort(returned_code)

    else:
        return jsonify({
            'success': True
        })
    
@users_bp.route('/user', methods=['POST'])
def verify_user():
    error_lists = []
    returned_code = 200
    try:
        body = request.get_json()

        if 'username' not in body:
            error_lists.append('username is required')
        else:
            username = body.get('username')

        if 'password' not in body:
            error_lists.append('password is required')
        else:
            password = body.get('password')

        user_db = User.query.filter(User.username == username).first()

        if user_db is None:
            error_lists.append('User not found')
        else:
            if user_db.verify_password(password) is False:
                error_lists.append('Incorrect password')

        if len(error_lists) > 0:
            returned_code = 400
        else:
            token = jwt.encode({
                'user_created_id': user_db.id,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=1440)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
        if returned_code == 400:
            return jsonify({
                'success': False,
                'errors': error_lists,
                'message': 'Error verifying user'
            }), returned_code
        else:
            return jsonify({
                'success': True,
                'token': token,
                'user_id': user_db.id,
            }), returned_code    
    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error verifying user'
        }), returned_code

