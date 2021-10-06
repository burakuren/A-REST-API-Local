from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user_r import (
    User_Register,
    User_Login,
    User,
    Token_Refresh
)
from resources.item_r import Item, Item_List
from resources.store_r import Store, Store_List

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["JWT_SECRET_KEY"] = "burak"
jwt = JWTManager()
jwt.init_app(app)


@jwt.expired_token_loader
def expired_token_callback(error):
    return {
        "message": "The token has expired",
        "error": "invalid_token"
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        "message": "Signature verification failed",
        "error": "invalid_token"
    }, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }, 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return {
        "description": "The token is not fresh",
        "error": "fresh_token_required"
    }, 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        "description": "The token has been revoked.",
        "error": "token_revoked"
    }, 401


api.add_resource(User_Register, "/register")
api.add_resource(User_Login, "/login")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(Token_Refresh, "/refresh")

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Item_List, "/items")

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Store_List, "/stores")


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
