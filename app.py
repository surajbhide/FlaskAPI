import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {'stores' : list(stores.values())}

@app.post("/store")
def create_store():
    store = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store, "id" : store_id}
    stores[store_id] = store
    return store, 201

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message=f"store {store_id} not found.")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": f"store with id {store_id} deleted."}
    except KeyError:
        abort(404, message=f"Store id {store_id} not found.")


@app.get("/item")
def get_items():
    return {"items" : list(items.values())}


@app.post("/item")
def create_item():
    item_data = request.get_json()
    store_id = item_data["store_id"]
    if store_id not in stores:
        abort(404, message=f"store {store_id} not found.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id" : item_id}
    items[item_id] = item
    return item, 201

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message=f"Item {item_id} not found.")
        
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "name" not in item_data or "price" not in item_data:
        abort(400, message="Bad request. Ensure 'price' and 'name' are in the JSON payload.")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": f"Item with id {item_id} deleted."}
    except KeyError:
        abort(404, message=f"Item id {item_id} not found.")