import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, UpdateItemSchema

blp = Blueprint("items", __name__, description= "Operations on Items.")

@blp.route('/item')
class Item(MethodView):
    def get(self):
        return {"items":list(items.values())}
    
    @blp.arguments(ItemSchema)
    def post(self, request_data):
        store_id = request_data['id']
        new_store = {**request_data, 'id': store_id}
        items[store_id] = new_store
        return {"items": new_store}

@blp.route('/item/<string:item_id>')
class ItemById(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='Item not found.')

    @blp.arguments(UpdateItemSchema)        
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Error item not found.")
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted"}
        except KeyError:
            abort(404, message='Item not found.')
