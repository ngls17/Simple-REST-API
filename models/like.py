import datetime

from flask_jwt import current_identity

from db import db


class LikeModel(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)

    def __init__(self, id_post):
        self.id_post = id_post
        self.id_user = current_identity.id
        self.date_created = datetime.datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_id_post_and_user(cls, id_post, id_user):
        return cls.query.filter_by(id_post=id_post, id_user=id_user).first()

    @classmethod
    def count_post_likes(cls, id_post):
        return cls.query.filter_by(id_post=id_post).count()

    @classmethod
    def find_all(cls):
        return cls.query.all()
