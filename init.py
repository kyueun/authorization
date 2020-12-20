from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, g, render_template_string
import jwt
from requests import Response
from DBmanage import *
from error import *

auth_app = Flask(__name__)
auth_app.config['SERVER_NAME'] = 'localhost:5000'
auth_app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'
auth_app.config['JWT_TOKEN_LOCATION'] = ['headers']
auth_app.secret_key = b'aXth_sXcrXt_kXX'


### authorization server

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is not None:
            try:
                payload = jwt.decode(access_token, auth_app.config['JWT_SECRET_KEY'], 'HS256')

            except jwt.InvalidTokenError:
                payload = None

            if payload is None:
                return Response(status=401)

            usr_email = payload['email']
            g.user_id = usr_email
            g.user = find_user(email=usr_email) if usr_email else None

        else:
            return 'Users Only'

        return f(*args, **kwargs)

    return decorated_function


def register_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is not None:
            try:
                payload = jwt.decode(access_token, auth_app.config['JWT_SECRET_KEY'], 'HS256')

                if not payload['registered']:
                    raise jwt.InvalidTokenError

            except jwt.InvalidTokenError:
                payload = None

            if payload is None:
                return Response(status=401)

            usr_email = payload['email']
            g.usr_email = usr_email
            g.usr = find_user(email=usr_email) if usr_email else None

        else:
            return 'Managers Only'

        return f(*args, **kwargs)
    return decorated_function


@auth_app.route('/')
def auth_home():
    return 'home'


@auth_app.route('/register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        data = request.form.to_dict()

        result = None
        try:
            register(email=data['email'], pw=data['pass'], name=data['name'])

            return redirect('/')

        except Exception as e:
            if type(e) is duplicate_user:
                result = 'registered account'

            elif type(e) is disable:
                result = 'try again'

        return render_template('register.html', msg=result)


@auth_app.route('/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        data = request.form.to_dict()

        result = None

        try:
            usr = login(email=data['email'], pw=data['pass'])

            payload = {
                'email': usr['email'],
                'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
            }

            token = jwt.encode(payload, auth_app.config['JWT_SECRET_KEY'], algorithm='HS256', headers={'Authorization': '*'})

            return jsonify({
                'access_token': token.decode('utf-8')
            })

        except Exception as e:
            if type(e) is no_user:
                result = 'no such user'

            else:
                print(type(e))
                print(e)
                result = 'try again'

        return render_template('login.html', msg=result)


@auth_app.route('/user', methods=['GET'])
@login_required
def auth_user():
    if request.method == 'GET':
        return 'hello, {}!'.format(g.user['name'])

    return 'Bad Request', 401


@auth_app.route('/manage', methods=['GET'])
#@register_required
def auth_manage():
    if request.method == 'GET':
        result = get_all_user()

        return

    return '??', 401


if __name__ == '__main__':
    auth_app.run(debug=True)
