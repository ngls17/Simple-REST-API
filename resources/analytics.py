import datetime
from utils import daterange

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.user import UserModel
from models.like import LikeModel
from db import db


class Analytics(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date_from',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('date_to',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    @jwt_required()
    def get(self):
        data = Analytics.parser.parse_args()
        likes = db.session.query(LikeModel.date_created, db.func.count(LikeModel.date_created)).filter(
            LikeModel.date_created > data['date_from'], LikeModel.date_created < data['date_to']).group_by(
            LikeModel.date_created).all()
        likes_dict = {date.date(): likes_count for date, likes_count in likes}

        result_stat = [{"date": date.strftime('%Y-%m-%d'), "likes": likes_dict.get(date) if likes_dict.get(date) else 0}
                       for date in
                       daterange(datetime.datetime.strptime(data['date_from'], "%Y-%m-%d").date(),
                                 datetime.datetime.strptime(data['date_to'], "%Y-%m-%d").date())]

        return result_stat, 200


class NumberOfUsers(Resource):
    @jwt_required()
    def get(self):
        print(UserModel.find_all())
        return {"number_of_users": len(UserModel.find_all())}, 200
