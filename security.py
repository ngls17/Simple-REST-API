import datetime

from werkzeug.security import safe_str_cmp
from models.user import UserModel

from db import db


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        user.last_login_time = datetime.datetime.now()
        db.session.commit()
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
