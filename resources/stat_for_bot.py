from flask_restful import Resource, reqparse

from models.user import UserModel
from models.post import PostModel
from models.like import LikeModel
from db import db


class NumberOfUsers(Resource):

    def get(self):
        print(UserModel.find_all())
        return {"number_of_users": len(UserModel.find_all())}, 200


class MaxPostsPerUser(Resource):

    def get(self):
        # get one post of each user
        users_posts = PostModel.query.group_by(PostModel.id_user).all()
        user_max_post = {"username": -1, "posts_number": 0}
        for post in users_posts:
            user_posts_count = PostModel.query.filter(PostModel.id_user == post.id_user).count()
            if user_posts_count > user_max_post["posts_number"]:
                user_max_post = {"username": UserModel.find_by_id(post.id_user).username,
                                 "posts_number": user_posts_count}
        if user_max_post["username"] == -1:
            return {'message': 'No posts found'}, 400
        return user_max_post, 200


class MaxLikesPerUser(Resource):

    def get(self):
        # get one like of each user
        users_likes = LikeModel.query.group_by(LikeModel.id_user).all()
        user_max_like = {"username": -1, "likes_number": 0}
        for like in users_likes:
            user_likes_count = LikeModel.query.filter(LikeModel.id_user == like.id_user).count()
            if user_likes_count > user_max_like["likes_number"]:
                user_max_like = {"username": UserModel.find_by_id(like.id_user).username,
                                 "likes_number": user_likes_count}
        if user_max_like["username"] == -1:
            return {'message': 'No likes found'}, 400
        return user_max_like, 200
