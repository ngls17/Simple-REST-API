from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.post import PostModel
from models.like import LikeModel


class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def post(self):
        data = Post.parser.parse_args()

        post = PostModel(data['text'])
        post.save_to_db()
        return {"message": "Post created successfully."}, 201

    @jwt_required()
    def get(self, _id):
        post = PostModel.find_by_id(_id)
        if post:
            return {"text": post.text, "likes": LikeModel.count_post_likes(_id), "id_user": post.id_user,
                    "date_created": post.date_created.strftime('%Y-%m-%d %H:%M')}, 200
        return {"message": "Wrong post id"}, 400


class Posts(Resource):
    @jwt_required()
    def get(self):
        return [{"id": post.id,
                 "text": post.text,
                 "id_user": post.id_user,
                 "date_created": post.date_created.strftime('%Y-%m-%d %H:%M')}
                for post in PostModel.find_all()], 200
