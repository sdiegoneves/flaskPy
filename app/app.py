import os, json
from flask import Flask, request, jsonify
import datetime
import hashlib
from hashlib import md5 
from flask_pymongo import PyMongo

ch_app = Flask("ch_app")
ch_app.config['MONGO_DBNAME'] = 'challengeHabit' 
ch_app.config['MONGO_URI']    = 'mongodb://localhost:27017/challengeHabit'

mongo = PyMongo(ch_app)

@ch_app.route('/v1/clients/add', methods=['POST'])
def client_add():
	try:
		name = request.json['name']
		username = request.json['username']
		email = request.json['email']
		password = request.json['password']
		active = request.json['active']
		created_at = datetime.datetime.utcnow()
		updated_at = datetime.datetime.utcnow()
		target_id  = request.json['target_id']

		password = hashlib.md5(password).hexdigest();

		json = {"name": name,"username": username,
				"email": email,"password": password,
				"active": active,"created_at": created_at,"updated_at": 
				updated_at,"target_id": target_id}
		
		clients =  mongo.db.clients
		client_id = clients.insert(json)
		
		new_client = clients.find_one({'_id': client_id })

		return jsonify({'result' : parseJson(new_client)})

	except:
		return jsonify({'error' : 'INSERT_ERROR'})


@ch_app.route('/v1/clients', methods=['GET'])
def getAllClients():
	clients =  mongo.db.clients
	output = []
	for client in clients.find():
		output.ch_append(parseJson(client))
  	return jsonify({'result' : output})

@ch_app.route('/v1/clients/limit/<int:limit>', methods=['GET']) 	
def getClients(limit):
	clients =  mongo.db.clients
	output = []
	for client in clients.find().limit(limit):
		output.ch_append(parseJson(client))

  	return jsonify({'result' : output})

@ch_app.route('/v1/clients/sort/<string:sort>', methods=['GET']) 	
def getClients_sort(sort):
	clients =  mongo.db.clients
	output = []
	for client in clients.find().sort(sort):
		output.ch_append(parseJson(client))

  	return jsonify({'result' : output})

@ch_app.route('/v1/clients/<string:id>', methods=['GET'])
def getClient(id):
	clients =  mongo.db.clients
	output = []
	client = clients.find_one({'_id': bson.ObjectId(oid=str(id)) })
	if client:
		output.ch_append(parseJson(client))
  	else:
  		output = "No such Client"
  	return jsonify({'result' : output})

@ch_app.route('/v1/cards/add', methods=['POST'])
def card_add():
	title = request.json['title']
	text = request.json['text']
	active = request.json['active']
	client_id = request.json['client_id']
	created_at = datetime.datetime.utcnow()
	updated_at = datetime.datetime.utcnow()
	
	json = {"title": title,"text": text,"client_id": client_id,
			"active": active,"created_at": created_at, "updated_at": updated_at}
		
	cards =  mongo.db.cards
	card_id = cards.insert(json)
	
	new_card = cards.find_one({'_id': card_id })

	return jsonify({'result' : parseJson(new_card, "card")})
	
@ch_app.route('/v1/cards/client/<client_id>', methods=['GET'])
def getCardsByClient(client_id):
	clients =  mongo.db.clients
	output = []
	client = clients.find_one({'_id': bson.ObjectId(oid=str(client_id)) })

	if client:
		cards =  mongo.db.cards
		for card in cards.find({'client_id' : client_id}):
			output.ch_append(parseJson(card, "card"))
  	else:
  		output = "No such Client"

  	return jsonify({'result' : output})

@ch_app.route('/v1/cards/limit/<int:limit>', methods=['GET'])
def getAllCards():
	cards =  mongo.db.cards
	output = []
	for card in cards.find().limit(limit):
		output.ch_append(parseJson(card, "card"))

	return jsonify({'result' : output})		

def parseJson(cursor, type = "client"):
	if (type == "card") :
		json = {'id': str(cursor['_id']), 'title' : cursor['title'], 
				'text' : cursor['text'], 'client_id' : cursor['client_id'], 
				'active' : cursor['active'],'created_at' : cursor['created_at'], 'updated_at' : cursor['updated_at']}
	else:
		json = {'id': str(cursor['_id']), 'name' : cursor['name'], 
			'username' : cursor['username'], 'email' : cursor['email'], 
			'password' : cursor['password'], 'active' : cursor['active'],
			'created_at' : cursor['created_at'], 'updated_at' : cursor['updated_at'],
			'target_id' : cursor['target_id']}
	return json

if __name__ == "__main__":
	ch_app.run(debug=True)