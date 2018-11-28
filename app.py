import os
from app import create_app
from models import *
from flask import request, jsonify, url_for
from bson.json_util import dumps
from bson.objectid import ObjectId

app = create_app()
Clients = Clients()

@app.route('/v1/clients/add', methods=['POST'])
def client_add():
	json = {"name": "UserAuto","username": "userNameauto","email": "emailUser","password": "passwordUser","active": True,"created_at": "2018-01-1 00:00:00","updated_at": "","target_id": ""}
	Clients.add(json);
	return "User Inserted"

@app.route("/v1/clients/<int:limit>")
def getClients(limit=10):
	clients = Clients.getClients(limit)
	cursor = dumps(clients)
	return cursor

@app.route("/v1/client/<id>")
def getClient(id):
	clients = Clients.getClient(id)
	cursor = dumps(clients)
	return cursor

if __name__ == "__main__":
	app.run(debug=True)