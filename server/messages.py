import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging


class Messages():
	
	def __init__(self):
		cred = credentials.Certificate('ASInt-Project-46914d756740.json')
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

