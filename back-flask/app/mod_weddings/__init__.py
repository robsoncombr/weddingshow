import os
import boto3 # http://boto3.readthedocs.io/en/latest/guide/s3.html
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from bson.objectid import ObjectId
from app.lib import token_required
from app import models
from app.mod_weddings import acl
from mongoengine.queryset.visitor import Q
# TODO: implementar a criação do thumbnail serverless, com trigger do S3
# https://santoshk.dev/posts/2021/create-thumbnail-worker-with-s3-and-lambda-make-the-thumbnail/
from PIL import Image

mod_weddings = Blueprint('weddings', __name__, url_prefix='/weddings')

@mod_weddings.route('', methods=['GET', 'POST'])
@mod_weddings.route('/<string:id_wedding>', methods=['GET', 'PUT', 'DELETE'])
@token_required
@acl.verify_wedding
def index(user, id_wedding=None):
    if request.method == 'GET':
      if id_wedding is None:
        # weddings = 'method to get a list of all weddings that user has access to'
        try:
          # NOTE: query evolution to get a list of all weddings that user has access to
          #weddings = models.Wedding.objects().filter(user=ObjectId(user['_id'])).order_by('-dt_created')
          #weddings = models.Wedding.objects().filter(users__email=user['email']).order_by('-dt_created')
          #weddings = models.Wedding.objects().filter(Q(user=ObjectId(user['_id']))).order_by('-dt_created')
          #weddings = models.Wedding.objects().filter(Q(users__email=user['email'])).order_by('-dt_created')
          #
          weddings = models.Wedding.objects().filter(Q(user=ObjectId(user['_id'])) | Q(users__email=user['email'])).order_by('-dt_created')
        except models.Wedding.DoesNotExist:
          return jsonify([]), 200
        #weddings = weddings.to_mongo()
        #wedding['_id'] = str(wedding['_id'])
        #wedding['user'] = str(wedding['user'])
        return jsonify(weddings), 200
      # return 'method to get wedding with id: ' + id_wedding, 200
      try:
        wedding = models.Wedding.objects.get(id=id_wedding)
      except models.Wedding.DoesNotExist:
        return 'Wedding does not exist', 404
      except models.Wedding.MultipleObjectsReturned:
        return 'Multiple weddings found', 400
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
        wedding['dt_created'] = datetime.utcnow()
        wedding['dt_updated'] = datetime.utcnow()
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
        return 'Multiple weddings found', 400
      except Exception as e:
        return str(e), 400
      wedding = wedding.to_mongo()
      wedding['_id'] = str(wedding['_id'])
      wedding['user'] = str(wedding['user'])
      return jsonify(wedding), 200
    if request.method == 'DELETE':
      # TODO: delete all S3 images before delete the document
      return 'method to delete wedding with id: ' + id_wedding, 200

@mod_weddings.route('/<string:id_wedding>/images/upload', methods=['POST'])
@token_required
@acl.verify_wedding_images
def upload(user, id_wedding, id_image=None):
    if request.method == 'POST':
      UPLOAD_FOLDER = "/tmp/uploads"
      BUCKET = "weddingshow.us-east-1"
      if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
      # return 'method to create/upload a new image to the wedding with id: ' + id_wedding, 200
      for fname in request.files:
        try:
          # url=f"https://s3.amazonaws.com/{BUCKET}/weddings/{id_wedding}/images/{f.filename}"
          image = models.Image(wedding=ObjectId(id_wedding), user=ObjectId(user['_id']), user_email=user['email'], dt_created=datetime.utcnow(), dt_updated=datetime.utcnow()).save()
          print(image)
          s3_client = boto3.client('s3')
          f = request.files.get(fname)
          filename = secure_filename(f.filename)
          src_file = os.path.join(UPLOAD_FOLDER, filename)
          dst_file = os.path.join(UPLOAD_FOLDER, f"thumb_{filename}")
          f.save(src_file)
          with Image.open(src_file) as image:
              image.thumbnail(tuple(x / 2 for x in image.size))
              image.save(dst_file)
          s3_client.upload_file(src_file, BUCKET, f"weddings/{id_wedding}/images/{filename}")
          s3_client.upload_file(dst_file, BUCKET, f"weddings/{id_wedding}/images/thumb_{filename}")
        except Exception as e:
          return str(e), 400
        return 'Image(s) uploaded', 200

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
      UPLOAD_FOLDER = "/tmp/uploads"
      BUCKET = "weddingshow-us-east-1"
      if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
      # return 'method to create/upload a new image to the wedding with id: ' + id_wedding, 200
      for fname in request.files:
        try:
          f = request.files.get(fname)
          print(f)
          #f.save('./uploads/%s' % secure_filename(fname))
          f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
          upload_file(f"{UPLOAD_FOLDER}/{f.filename}", BUCKET, f.filename)
        except Exception as e:
          return str(e), 400
        return 'ok', 200
    if request.method == 'DELETE':
      return 'method to delete image with id: ' + id_image + ' from the wedding with id: ' + id_wedding, 200
