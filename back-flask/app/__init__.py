# import flask
from flask import Flask, render_template
# import cors
from flask_cors import CORS
# import session
from flask_session import Session
# import websocket
from flask_sock import Sock
# import mongoengine
from flask_mongoengine import MongoEngine
# Import SQLAlchemy
#from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# configurations
app.config.from_object('config')

# cors
CORS(app)

# websocket
sock = Sock(app)
@sock.route('/ws/echo')
def ws_echo(sock):
    while True:
        data = sock.receive()
        sock.send(data)
@app.route('/ws')
def ws_index():
    return render_template('ws-demo.html')

# mongoengine
db = MongoEngine(app)

# Define the database object which is imported
# by modules and controllers
#db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

from app import lib
# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()