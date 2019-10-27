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


    @staticmethod
    def user_from_token(token):
        decode_result = TokenAuth.decode_token(token)
        email = decode_result.get("user_email", "")

        if not email:
            return { "error": "invalid token" }

        user_entry = User.query.filter_by(email=email).first()

        if not user_entry:
            return { "error": "invalid token" }
        else:
            return { "success": user_entry }