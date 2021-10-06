from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from models.user_m import User_Model

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field cannot be blank!"
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be blank!"
)


class User_Register(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if User_Model.find_by_username(data["username"]):
            return {"message": "A user with this username is already exists"}, 400

        new_user = User_Model(data["username"], data["password"])
        new_user.save_to_db()

        return {"message": "User is created successfully!"}, 201


class User_Login(Resource):

    def post(self):
        data = _user_parser.parse_args()

        login_user = User_Model.find_by_username(data["username"])

        if login_user and login_user.password == data["password"]:
            access_token = create_access_token(identity=login_user.id, fresh=True)
            refresh_token = create_refresh_token(login_user.id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "Your username or password is wrong!"}, 401


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = User_Model.find_by_id(user_id)
        if not user:
            return {"message": "User Not Found!"}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = User_Model.find_by_id(user_id)
        if not user:
            return {"message": "User Not Found"}, 404
        user.delete_from_db()
        return {"message": "User deleted."}, 200


class Token_Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
