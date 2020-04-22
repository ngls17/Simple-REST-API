import datetime
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity

from models.post import PostModel
from models.like import LikeModel
from db import db


class Like(Resource):

    @jwt_required()
    def put(self, id_post):
        post = PostModel.find_by_id(id_post)
        if not post:
            return {"message": "Post does not exist"}, 400
        liked = LikeModel.find_by_id_post_and_user(id_post, current_identity.id)
        if not liked:
            like = LikeModel(id_post)
            like.save_to_db()
            return {"message": "Post liked"}, 201
        else:
            liked.date_created = datetime.datetime.now()
            return {"message": "Post liked again"}, 200
        return {"message": "Error"}, 400

    @jwt_required()
    def get(self, id_post):
        like = LikeModel.find_by_id(id_post)
        if like:
            return {"id_post": like.id_post, "id_user": like.id_user,
                    "date_created": like.date_created.strftime('%Y-%m-%d %H:%M')}, 200
        return {"message": "Post not liked yet"}, 400

    @jwt_required()
    def delete(self, id_post):
        post = PostModel.find_by_id(id_post)
        if not post:
            return {"message": "Post does not exist"}, 400
        liked = LikeModel.find_by_id_post_and_user(id_post, current_identity.id)
        if liked:
            LikeModel.query.filter_by(id_post=id_post, id_user=current_identity.id).delete()
            db.session.commit()
            return {"message": "Post unliked"}, 201
        return {"message": "Post not liked yet"}, 400


class Likes(Resource):
    @jwt_required()
    def get(self):
        return [{"id": like.id,
                 "id_post": like.id_post,
                 "id_user": like.id_user,
                 "date_created": like.date_created.strftime('%Y-%m-%d %H:%M')}
                for like in LikeModel.find_all()], 200
