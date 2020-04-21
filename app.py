from __init__ import app, api, jwt

import datetime

from flask_jwt import current_identity

from resources.user import UserRegister, GetUsers, UserActivity
from resources.post import Post
from resources.like import Like
from resources.analytics import Analytics
from models.user import UserModel

api.add_resource(UserRegister, '/register')
api.add_resource(GetUsers, '/users')
api.add_resource(UserActivity, '/user/activity/<string:username>')
api.add_resource(Post, '/post/<int:_id>', '/post')
api.add_resource(Like, '/like/<int:id_post>')
api.add_resource(Analytics, '/analytics')

@app.before_first_request
def create_tables():
    db.create_all()


@app.after_request
def save_request_date(response):
    if current_identity:
        current_identity.last_activity_time = datetime.datetime.now()
        db.session.commit()
    return response


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)