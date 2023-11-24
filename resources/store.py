import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, StoreSchemaPost

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    blp.response(200, StoreSchema)
    def get(self, store_id):
        try:    
            return stores[store_id]
        except KeyError:
            return {'error': 'Store not found.', "Stores": stores}
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found with the mentioned id.")

@blp.route("/store")
class Store_All(MethodView):
    def get(self):
        return {"stores" : list(stores.values())}
    
    @blp.arguments(StoreSchemaPost)
    def post(self, store_data):
        for store in stores.values():
            if store_data['name'] == store['name']:
                abort(400, message="Store name already present.")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, 'id': store_id}
        stores[store_id] = new_store
        return new_store
