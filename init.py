from flask import Flask, render_template, request
from flask_jwt_extended import *
from multiprocessing import Process

auth_app = Flask(__name__)
auth_app.config['SERVER_NAME'] = 'localhost:5000'
auth_app.secret_key = b'aXth_sXcrXt_kXX'

api_app = Flask(__name__)
api_app.config['SERVER_NAME'] = 'localhost:5001'
api_app.secret_key = b'apX_sXcrXt_kXX'


### authorization server

@auth_app.route('/')
def home():
    return "render_template('index.html')"


@auth_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'register::get'
    elif request.method == 'POST':
        return 'register::post'


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'login::get'
    elif request.method == 'POST':
        return 'login::post'


@auth_app.route('/user', methods=['GET'])
@jwt_required
def user():
    if request.method == 'GET':
        return 'user::get'


@auth_app.route('/manage', methods=['GET'])
@jwt_required
def manage():
    if request.method == 'GET':
        return 'manage::get'


def start_auth(debug, port):
    auth_app.run(debug=debug, port=port)


### api server

@api_app.route('/')
def api_home():
    return 'api_home'


@api_app.route('/create/<id>', methods=['GET'])
def create(id):
    if request.method == 'GET':
        return 'create::get, id={}'.format(id)


@api_app.route('/refresh/<id>', methods=['GET'])
def refresh(id):
    if request.method == 'GET':
        return 'refresh::get, id={}'.format(id)


def start_api(debug, port):
    api_app.run(debug=debug, port=port)


def process(target, args):
    proc = Process(target=target, args=args)
    proc.daemon = True
    proc.start()

    return proc


if __name__ == '__main__':
    auth_p = process(target=start_auth, args=(False, 5000))
    api_p = process(target=start_api, args=(False, 5001))

    auth_p.join()
    api_p.join()
