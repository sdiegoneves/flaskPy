from mongo_connect import mongo
from bson.objectid import ObjectId


class Clients():

	def add(self, data):
		return mongo.db.clients.insert_one(str(data)).inserted_id
	
	def getClient(self, id):
		return mongo.db.clients.find_one({"_id": ObjectId(id)})

	def getClients(self, limit, sorted=None):
		return mongo.db.clients.find().limit(limit)

class Cards(): 
	def add(self) :
		return mongo.db.cards.insert_one(str(data)).inserted_id

	def getCard(self, uid):
		return mongo.db.cards.find_one({"_id": ObjectId(id)})

	
	def getCards(self, order, limit, where):
		return mongo.db.cards.find().limit(limit)
