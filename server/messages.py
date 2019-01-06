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

	def sendToBuilding(self, data, id, bid, bot = 0):
		if bot == 0:
			c = self.datastore.getUserCoords(id)
			data['sender'] = id
			self.datastore.addLog(id, c[0], c[1], bid, message=data)

		if bid == None:
			return

		for user in self.datastore.listBuildingUsersID(bid):
			if user != id:
				data['sender'] = id
				c = self.datastore.getUserCoords(user)
				self.datastore.addLog(user, c[0], c[1], bid, message=data)
				self.sendMessage(data['message'],id,self.datastore.userToken(user))

	def sendToNearby(self,data, id):

		bid = self.datastore.userBuilding(id)
		c = self.datastore.getUserCoords(id)
		data['sender'] = id
		self.datastore.addLog(id, c[0], c[1], bid, message=data)

		for user in self.datastore.usersNearbyID(id):
			if user != id:
				data['sender'] = id
				c = self.datastore.getUserCoords(user)
				self.datastore.addLog(user, c[0], c[1], bid, message=data)
				self.sendMessage(data['message'],id,self.datastore.userToken(user))