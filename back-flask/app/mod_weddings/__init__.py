from crypt import methods
from flask import Blueprint, request, jsonify

mod_weddings = Blueprint('weddings', __name__, url_prefix='/weddings')

@mod_weddings.route('/', methods=['GET', 'POST'])
@mod_weddings.route('/<string:id_wedding>', methods=['GET', 'PUT', 'DELETE'])
def index(id_wedding=None):
    if request.method == 'GET':
      if id_wedding is None:
        weddings = 'method to get a list of all weddings that user has access to'
        return jsonify(weddings), 200
      return 'method to get wedding with id: ' + id_wedding, 200
    if request.method == 'POST':
      return 'method to create a new wedding', 200
    if request.method == 'PUT':
      return 'method to update wedding with id: ' + id_wedding, 200
    if request.method == 'DELETE':
      return 'method to delete wedding with id: ' + id_wedding, 200

@mod_weddings.route('/<string:id_wedding>/users', methods=['GET', 'POST'])
@mod_weddings.route('/<string:id_wedding>/users/<string:email_user>', methods=['PUT', 'DELETE'])
def users(id_wedding, email_user=None):
    if request.method == 'GET':
      if email_user is None:
        users = 'method to get a list of all users that has access to the wedding with id: ' + id_wedding
        return jsonify(users), 200
    if request.method == 'POST':
      return 'methods to add access to a new user to the wedding with id: ' + id_wedding, 200
    if request.method == 'PUT':
      return 'method to update user with email: ' + email_user + ' to the wedding with id: ' + id_wedding, 200
    if request.method == 'DELETE':
      return 'method to delete user with email: ' + email_user + ' from the wedding with id: ' + id_wedding, 200
