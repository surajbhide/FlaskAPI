from email import message
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required

from models.store import StoreModel
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Stores", __name__, description="Operations on store")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema())
    @blp.response(201, StoreSchema)
    def post(self, store):
        new_store = StoreModel(**store)
        print(f"**** {new_store}")
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="Error inserting store.")
        print(new_store)
        return new_store
    
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store was deleted."}
            
            
