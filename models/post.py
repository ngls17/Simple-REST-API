import datetime

from flask_jwt import current_identity

from db import db


class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    id_user = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)

    def __init__(self, text):
        self.text = text
        self.id_user = current_identity.id
        self.date_created = datetime.datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
