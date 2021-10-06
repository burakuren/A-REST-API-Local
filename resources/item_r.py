from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from models.item_m import Item_Model


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be blank!"
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="This field cannot be blank!"
    )

    @jwt_required()
    def get(self, name: str):
        item = Item_Model.find_by_name(name)

        if item:
            return item.json()
        return {"message": "Item not found!"}, 404

    @jwt_required(fresh=True)
    def post(self, name: str):
        if Item_Model.find_by_name(name):
            return {"message": "An item with name {} is already exists".format(name)}, 400

        data = self.parser.parse_args()

        item = Item_Model(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name: str):
        item = Item_Model.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}, 201
        return {"message": "Item not found."}, 404

    def put(self, name):
        data = self.parser.parse_args()

        item = Item_Model.find_by_name(name)

        if item:
            item.price = data["price"]

        else:
            item = Item_Model(name, **data)

        item.save_to_db()

        return item.json()


class Item_List(Resource):

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in Item_Model.find_all()]
        if user_id:
            return {"items": items}, 200
        return {
            "items": [item["name"] for item in items],
            "message": "More data available if you log in."
        }, 200
