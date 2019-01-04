import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

from datastore import *

class Messages():
	
	def __init__(self, datastore):
		self.datastore = datastore;
		cred = credentials.Certificate('credentials.json')
		self.app = firebase_admin.initialize_app(cred)

	def sendMessage(self, data, sender, utoken):
		message = messaging.Message(
		    data={
		        'message': data,
		        'sender': sender,
		    },
		    token=utoken,
		)
		response = messaging.send(message)

	def sendToBuilding(self, data, id):
		token = self.datastore.userToken(id)
		bid = self.datastore.userBuilding(id)

		for user in self.datastore.listBuildingUsers(bid):
			if user != id:
				self.sendMessage(data,id,self.datastore.userToken(user))

	def sendToNearby(self,data, id):
		token = self.datastore.userToken(id)
		bid = self.datastore.userBuilding(id)

		for user in self.datastore.usersNearby(bid):#TODO IN DATASTORE
			if user != id:
				self.sendMessage(data,id,self.datastore.userToken(user))