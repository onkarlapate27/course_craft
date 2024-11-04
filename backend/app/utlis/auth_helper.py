import jwt
import logging
from datetime import datetime, timedelta
from courses.config_settings import settings

def encode_jwt(user_id, role):
    try:
        payload = {
            'user_id': user_id,
            'role': role,
            'expiry': (datetime.utcnow() + timedelta(hours=24)).timestamp(),
            'iat': datetime.utcnow().timestamp()
        }
        encoded_token = jwt.encode(payload=payload, key=settings.get('JWT_SECRET'), algorithm=settings.get('JWT_ALGORITHM'))
        return encoded_token
    except Exception as e:
        logging.error("Unable to encode jwt token.")
        logging.error(e)

def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token)
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        logging.error("Token expired.")
    except jwt.InvalidTokenError:
        logging.error("Invalid token.")

def validate_password(password):
    message = ""
    is_password_valid = True

    if not isinstance(password, str):
        message = "Password should be string"
        is_password_valid = False

    elif len(password) < 8:
        message = "Password needs to be atleast 8 characters long."
        is_password_valid = False

    return is_password_valid, message