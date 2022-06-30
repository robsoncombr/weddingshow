from flask import Blueprint, request, jsonify
from datetime import datetime
from bson.objectid import ObjectId
from app.lib import token_required
from app import models
from app.mod_weddings import acl

mod_weddings = Blueprint('weddings', __name__, url_prefix='/weddings')

@mod_weddings.route('', methods=['GET', 'POST'])
@mod_weddings.route('/<string:id_wedding>', methods=['GET', 'PUT', 'DELETE'])
@token_required
@acl.verify_wedding
def index(user, id_wedding=None):
    if request.method == 'GET':
      if id_wedding is None:
        weddings = 'method to get a list of all weddings that user has access to'
        return jsonify(weddings), 200
      # return 'method to get wedding with id: ' + id_wedding, 200
      try:
        wedding = models.Wedding.objects.get(id=id_wedding)
      except models.Wedding.DoesNotExist:
        return 'Wedding does not exist', 404
      wedding = wedding.to_mongo()
      wedding['_id'] = str(wedding['_id'])
      wedding['user'] = str(wedding['user'])
      return jsonify(wedding), 200
    if request.method == 'POST':
      # return 'method to create a new wedding', 200
      try:
        wedding = models.Wedding(**request.json)
        wedding['user'] = ObjectId(user['_id'])
        if not wedding['users']:
          wedding['users'] = []
        wedding.save()
      except Exception as e:
        return str(e), 400
      wedding = wedding.to_mongo()
      wedding['_id'] = str(wedding['_id'])
      wedding['user'] = str(wedding['user'])
      return jsonify(wedding), 200
    if request.method == 'PUT':
      # return 'method to update wedding with id: ' + id_wedding, 200
      try:
        wedding = models.Wedding.objects.get(id=id_wedding)
        # TODO: block fields that can not be changed
        wedding['user'] = ObjectId(user['_id'])
        request.json['dt_updated'] = datetime.utcnow()
        wedding.update(**request.json)
      except models.Wedding.DoesNotExist:
        return 'Wedding does not exist', 404
      except models.Wedding.MultipleObjectsReturned:
        return 'Multiple weddings with same id', 400
      except Exception as e:
        return str(e), 400
      wedding = wedding.to_mongo()
      wedding['_id'] = str(wedding['_id'])
      wedding['user'] = str(wedding['user'])
      return jsonify(wedding), 200
    if request.method == 'DELETE':
      # TODO: delete all S3 images before delete the document
      return 'method to delete wedding with id: ' + id_wedding, 200

@mod_weddings.route('/<string:id_wedding>/images', methods=['GET', 'POST'])
@mod_weddings.route('/<string:id_wedding>/images/<string:id_image>', methods=['DELETE'])
@token_required
@acl.verify_wedding_images
def images(user, id_wedding, id_image=None):
    if request.method == 'GET':
      if id_image is None:
        images = 'method to get a list of all images that the user has access to the wedding with id: ' + id_wedding
        # NOTE: the list will include all approved and uploaded by the user: { wedding: [], user: []}
        return jsonify(images), 200
    if request.method == 'POST':
      return 'method to create/upload a new image to the wedding with id: ' + id_wedding, 200
    if request.method == 'DELETE':
      return 'method to delete image with id: ' + id_image + ' from the wedding with id: ' + id_wedding, 200
