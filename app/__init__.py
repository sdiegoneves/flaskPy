import os, json
from flask import Flask, request, jsonify
import datetime
import hashlib
from hashlib import md5 
from flask_pymongo import PyMongo

ch_app = Flask("ch_app")
def create_app():
	return ch_app

def create_mongo():
	ch_app.config['MONGO_DBNAME'] = 'challengeHabit' 
	ch_app.config['MONGO_URI']    = 'mongodb://localhost:27017/challengeHabit'

	mongo = PyMongo(ch_app)

	return mongo