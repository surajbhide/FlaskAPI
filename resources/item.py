import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        store_id = item_data["store_id"]
        if store_id not in stores:
            abort(404, message=f"store {store_id} not found.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id" : item_id}
        items[item_id] = item
        return item, 201

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message=f"Item {item_id} not found.")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="item not found.")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"Item with id {item_id} deleted."}
        except KeyError:
            abort(404, message=f"Item id {item_id} not found.")