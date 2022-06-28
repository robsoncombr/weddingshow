# Import flask dependencies
from flask import Blueprint, jsonify, request, current_app, render_template, \
    flash, g, session, redirect, url_for

from datetime import datetime, timedelta

import jwt

# import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import the database object from the main app module
from app import db, models

# Import module forms
from app.mod_auth.forms import LoginForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# ref: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

@mod_auth.route('/signup/', methods=['POST'])
def signup():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    if name is None:
        return 'Missing name', 400
    elif email is None or password is None:
        return 'Missing username or password', 400
    # TODO: validate email format and password strength
    try:
        user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        user = models.User(name=name, email=email, password=generate_password_hash(password))
        user.save()
        user = user.to_mongo()
        user['_id'] = str(user['_id'])
        del user['password']
        #return user, 201
        return 'User created', 201
    return 'User already exists', 400

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return 'Missing username or password', 400
    try:
        user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        return 'User does not exist', 400
    user = user.to_mongo()
    user['_id'] = str(user['_id'])
    if check_password_hash(user['password'], password):
        del user['password']
        '''
        ref: https://pyjwt.readthedocs.io/en/stable/usage.html
        I create the JWT token using PyJWT (as jwt) by encoding a dictionary containing the following:
        sub - the subject of the jwt, which in this case is the user's email
        iat - the time the jwt was issued at
        exp - is the moment the jwt should expire, which is 30 minutes after issuing in this case
        '''
        token = jwt.encode({
            'sub': email,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
            current_app.config['SECRET_KEY'], algorithm='HS256')
        #print(jwt.decode(token, current_app.config['SECRET_KEY'], 'HS256'))
        return jsonify({ 'token': token }), 200
    return 'Wrong password', 400

@mod_auth.route('/user/', methods=['GET', 'POST'])
def user():
    if 'username' not in session:
        return 'Unauthorized', 401
    if request.method == 'GET':
        return session['username']
    return 'TODO: implement POST'
