import functools
from flask import Response
from datetime import datetime
from uuid import UUID

from db import db
from models.auth_tokens import AuthTokens


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)

        return True
    except:

        return False


def validate_token(arg_zero):
    auth_token = arg_zero.headers['auth']

    if not auth_token or not validate_uuid4(auth_token):

        return False

    auth_record = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if auth_record:
        if auth_record.expiration > datetime.utcnow():
            return auth_record

        else:
            return False


def fail_response():
    return Response("authentication required", 401)


def authenticate(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return


def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])
        kwargs["auth_info"] = auth_info

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return
