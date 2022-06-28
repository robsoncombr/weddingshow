from flask import current_app, request, jsonify
from datetime import datetime, timedelta
from functools import wraps # functools is a standard Python module for higher-order functions (functions that act on or return other functions). wraps() is a decorator that is applied to the wrapper function of a decorator.
import jwt
from app import models

def token_create(**kwargs):
        email = kwargs.get('email')
        '''
        ref: https://pyjwt.readthedocs.io/en/stable/usage.html
        #
        I create the JWT token using PyJWT (as jwt) by encoding a dictionary containing the following:
        sub - the subject of the jwt, which in this case is the user's email
        iat - the time the jwt was issued at
        exp - is the moment the jwt should expire, which is 120 minutes after issuing in this case
        #
        I will not create a refresh token for now and I will use the JWT token for the authentication and also for the refresh token.
        '''
        token = jwt.encode({
            'sub': email,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=120)},
            current_app.config['SECRET_KEY'], algorithm='HS256')
        #print(jwt.decode(token, current_app.config['SECRET_KEY'], 'HS256'))
        return jsonify({ 'token': token })

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401
        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], 'HS256')
            user = models.User.objects.get(email=data['sub'])
            user = user.to_mongo()
            user['_id'] = str(user['_id'])
            del user['password']
        except models.User.DoesNotExist:
            raise RuntimeError('User not found')
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
        return f(user, *args, **kwargs)
    return _verify