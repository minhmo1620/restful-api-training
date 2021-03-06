from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float,
		required=True,
		help="Cannot be left blank!")

	parser.add_argument('store_id', 
		type=int,
		required=True,
		help="Cannot be left blank!")

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message':'Item not found'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name) != None:
			return {'message':'Existed item'}, 400

		request_data = Item.parser.parse_args()
		item = ItemModel(name, request_data['price'], request_data['store_id'])
		
		try:
			item.save_to_db()
		except:
			return {'message':'An error occurred in inserting item'}, 500
		return item.json(),201

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		return {'message': 'Item deleted'}

	def put(self, name):

		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']

		item.save_to_db()
		return item.json() 

class ItemList(Resource):
	def get(self):

		return {'items': [u.json() for u in ItemModel.query.all()]}