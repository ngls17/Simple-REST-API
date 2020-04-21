from db import db
import datetime
from flask_jwt import current_identity


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

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
