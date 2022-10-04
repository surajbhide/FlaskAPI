import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on store")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema())
    @blp.response(201, StoreSchema)
    def post(self, store):
        for item in stores.values():
            if store['name'] == item['name']:
                abort(400, message="Bad request. Store already exists.")
        store_id = uuid.uuid4().hex
        store = {**store, "id" : store_id}
        stores[store_id] = store
        return store, 201
    
@blp.route("/store/<string:store_id>")
class StoreItem(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message=f"store {store_id} not found.")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": f"store with id {store_id} deleted."}
        except KeyError:
            abort(404, message=f"Store id {store_id} not found.")
            
            
