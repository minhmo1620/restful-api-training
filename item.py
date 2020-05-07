import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float,
		require=True,
		help="Cannot left blank!")

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()

		if row:
			return {'item':{'name': row[0], 'price': row[1]}}, 200

	@jwt_required()
	def get(self, name):
		row = self.find_by_name(name)
		if row:
			return {'item':{'name': row[0], 'price': row[1]}}, 200
		return {'message':'Item not found'}, 404

	def post(self, name):
		if self.find_by_name(name) != None:
			return {'message':'Existed item'}, 400

		request_data = Item.parser.parse_args()
		item = {'name':name, 'price': request_data['price']}
		
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(query, (item['name'], item['price'],))

		cursor.commit()
		cursor.close()

		return item,201

	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		cursor.commit()
		cursor.close()

		return {'message': 'Item deleted'}

	def put(self, name):

		data = Item.parser.parse_args()

		item = next(filter(lambda x: x['name'] == name, items), None)

		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)

		else:
			item.update(data)
		return item 

class ItemList(Resource):
	def get(self):
		return {'items':items}