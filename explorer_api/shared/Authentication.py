import jwt
import os

from datetime import datetime, timedelta

from ..models.User import User


class TokenAuth():

    @staticmethod
    def generate_token(user_email):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),   # expires at
                'iat': datetime.utcnow(),                       # issued at
                'sub': user_email                               # subject
            }
            token = jwt.encode(
                payload,
                os.environ['JWT_KEY'],
                algorithm='HS256'
            ).decode("utf-8")
            return { 'token': token }
        except:
            return { 'error': 'could not generate user token' }


    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(
                token, 
                os.environ['JWT_KEY'],
                algorithms=['HS256']
            )
            return { 'user_email': payload['sub'] }
        except KeyError:
            return { 'error': 'wrong token format' }
        except jwt.ExpiredSignatureError:
            return { 'error': 'token expired, please login again' }
        except jwt.InvalidTokenError:
            return { 'error': 'invalid token' }