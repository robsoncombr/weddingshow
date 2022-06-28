import jwt
from flask import current_app, jsonify
from datetime import datetime, timedelta

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