from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class Users(Resource):
    def get(self):
        print(current_identity)
        return [{"username": user.username, "password": user.password} for user in UserModel.find_all()], 200


class UserActivity(Resource):
    @jwt_required()
    def get(self, username):
        if UserModel.find_by_username(username):
            user = UserModel.find_by_username(username)
            return {"last_login_time": user.last_login_time.strftime(
                '%Y-%m-%d %H:%M') if user.last_login_time else None,
                    "last_activity_time": user.last_activity_time.strftime(
                        '%Y-%m-%d %H:%M') if user.last_activity_time else None}, 200
        return {"message": "Wrong username"}, 400
