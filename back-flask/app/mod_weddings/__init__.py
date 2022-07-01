import os
import base64
import boto3 # http://boto3.readthedocs.io/en/latest/guide/s3.html
from tabnanny import filename_only
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from io import BytesIO
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
      BUCKET = "weddingshow.us-east-1"
      UPLOAD_FOLDER = "/tmp/uploads"
      if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
      # return 'method to create/upload a new image to the wedding with id: ' + id_wedding, 200
      for fname in request.files:
        try:
          s3_client = boto3.client('s3')
          file = request.files.get(fname)
          filename = secure_filename(file.filename)
          db_image = models.Image(wedding=ObjectId(id_wedding), user=ObjectId(user['_id']), user_email=user['email'], filename=filename, dt_created=datetime.utcnow(), dt_updated=datetime.utcnow()).save()
          db_image_mongo = db_image.to_mongo()
          print('created on database: ' + filename)
          filename = f"{db_image_mongo['_id']}_{filename}"
          src_file = os.path.join(UPLOAD_FOLDER, filename)
          filename_only, file_extension = os.path.splitext(src_file)
          file.save(src_file)
          print('saved to disk: ' + src_file)
          with Image.open(src_file) as image:
              image.thumbnail(tuple(x / 2 for x in image.size))
              try:
                # https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array
                imgByteArr = BytesIO()
                image.save(imgByteArr, format=image.format)
                db_image.thumb = imgByteArr.getvalue()
                db_image.save()
                print('saved thumb on db: ' + src_file)
              except Exception as e:
                print(str(e))
                return str(e), 400
          s3_client.upload_file(src_file, BUCKET, f"weddings/{id_wedding}/images/{filename}")
          print(f"saved to s3: weddings/{id_wedding}/images/{filename}")
          os.remove(src_file)
          print('removed from disk: ' + src_file)
        except Exception as e:
          print(str(e))
          return str(e), 400
      return 'Image(s) uploaded', 200

@mod_weddings.route('/<string:id_wedding>/images/user', methods=['GET'])
@token_required
@acl.verify_wedding_images
def list_images_user(user, id_wedding):
    if request.method == 'GET':
      try:
        images = models.Image.objects().filter(Q(wedding=ObjectId(id_wedding)) & Q(user=ObjectId(user['_id']))).order_by('dt_created')
      except Exception as e:
        print(str(e))
        return str(e), 400
      return jsonify(images), 200

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
