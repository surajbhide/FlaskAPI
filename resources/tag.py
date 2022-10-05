from ast import Delete
from re import X
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tag", __name__, description="operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)    
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
            abort(400, message="Tag with that name exists in that store already.")
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return tag
    
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        if item.store.id != tag.store.id:
            abort(400, "Item and tag don't seem to belong to same store.")
        
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "Error while linkig tag to item")
        
        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "unable to delink tag from item")
        return {"message" : "Tag and Item delinked", "item" : item, "tag" : tag}

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="deletes a tag if no items are linked to it.", example={"message": "tag deleted."})
    @blp.alt_response(404, description="tag not found")
    @blp.alt_response(400, description="Returned if tag is linked to items. in this case tag can't be deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message" : "tag deleted."}
        abort(400, message="Could not delete tag. Make sure tag is not associated with any items, then try again.")