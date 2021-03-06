# Import flask dependencies
from flask import Blueprint, jsonify, request, current_app, render_template, \
    flash, g, session, redirect, url_for

from datetime import datetime

# import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import the database object from the main app module
from app import models

from app.lib import token_create, token_required

# Import module forms
from app.mod_auth.forms import LoginForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# ref: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

@mod_auth.route('/signup', methods=['POST'])
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
        user = models.User(name=name, email=email, password=generate_password_hash(password), dt_created=datetime.utcnow(), dt_updated=datetime.utcnow()).save()
        user.save()
        user = user.to_mongo()
        user['_id'] = str(user['_id'])
        del user['password']
        #return user, 201
        #return 'User created', 201
        token = token_create(email=email)
        return jsonify({ 'user': user, 'token': token }), 200
    return 'User already exists', 400

@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return 'Missing username or password', 400
    try:
        user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        return 'User does not exist', 401
    user = user.to_mongo()
    user['_id'] = str(user['_id'])
    if check_password_hash(user['password'], password):
        token = token_create(email=email)
        return jsonify({ 'token': token }), 200
    return 'Wrong password', 401

@mod_auth.route('/user', methods=['GET', 'POST'])
@token_required
def user(current_user):
    if request.method == 'GET':
        return current_user, 200
    return 'POST'

@mod_auth.route('/user/token_refresh', methods=['GET'])
@token_required
def user_token(current_user):
    if request.method == 'GET':
        token = token_create(email=current_user['email'])
        return jsonify({ 'token': token }), 200