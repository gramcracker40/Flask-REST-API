import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
        except AttributeError as err:
            abort(404, message=f"{err} Store with specified ID not found")
        return {"message":"store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        all = StoreModel.query.all()
        return all

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        print(f"Store data: {store_data}")
        store = StoreModel(**store_data)
       
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message=f"A store with name '{store_data['name']}' already exists")
        except SQLAlchemyError as err:
            abort(500, message=f"An error occurred in processing - {err}")
        
        return 'OK'
        #return f"Successfully added store '{store_data['name']}'"