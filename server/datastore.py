from google.cloud import datastore
from numpy import linalg as LA
import datetime

buildingEnt = 'building'
logEnt = 'log'
userEnt = 'user'
botEnt = 'bot'

class Datastore:
	def __init__(self):
		self.client = datastore.Client.from_service_account_json('credentials.json')

#------------------Buildings---------------------

	def addBuilding(self, id, name, x, y):
		key = self.client.key(buildingEnt,int(id))
		building = datastore.Entity(key)
		building.update({
			'name': name,
			'x': x,
			'y': y,
			'users': []
		})
		self.client.put(building)
		return

	def showBuilding(self, b_id):
		key = self.client.key(buildingEnt, b_id)
		building = self.client.get(key)
		return building

	def listAllBuildings(self):
		query = self.client.query(kind=buildingEnt)
		return list(query.fetch())

	def listBuildingUsers(self, b_id):
		key = self.client.key(buildingEnt, b_id)
		building = self.client.get(key)
		return building['users']

	def addUserToBuilding(self, b_id, user_id):
		key = self.client.key(buildingEnt, b_id)
		building = self.client.get(key)
		if user_id not in building['users']:
			building['users'].append(user_id)
			self.client.put(building)
		return

	def removeUserFromBuilding(self, b_id, user_id):
		key = self.client.key(buildingEnt, b_id)
		building = self.client.get(key)
		building['users'].remove(user_id)
		self.client.put(building)
		return

	def isUserinBuilding(self,x,y, user_id):
		try:
			nearby = self.userNearby(user_id)
		except Exception as e:
			nearby = 10 #DEFAULT

		for building in self.listAllBuildings():
			r = LA.norm((float(x)-float(building['x']),float(y)-float(building['y'])))
			if r < nearby:
				return building.key.id
		return 0

	def updateUserBuilding(self,x,y,userid):
		bid = self.isUserinBuilding(x,y,userid)
		try:
			if self.userBuilding(userid) != bid:
				self.removeUserFromBuilding(self.userBuilding(userid), userid)
		except Exception as e:
			pass
			self.addLog(userid, x, y,building = bid)
		try:
			self.addUserToBuilding(bid,userid)
		except Exception as e:
			pass
		return
#------------------User---------------------
	
	def addUser(self, user_id):
		key = self.client.key(userEnt, user_id)
		if self.client.get(key) == None:
			user = datastore.Entity(key)
			user['nlogs'] = 0
			user['nearby'] = 10
			user['token'] = -1
			self.client.put(user)
		return

	def setUserToken(self, user_id, utoken):
		key = self.client.key(userEnt, user_id)
		if self.client.get(key) == None:
			return 0
		else:
			user = self.client.get(key)
			user['token'] = utoken
			self.client.put(user)
		return 1

	def userToken(self, user_id):
		key = self.client.key(userEnt, user_id)
		if self.client.get(key) == None:
			return 0
		else:
			user = self.client.get(key)	
			return user['token']

	def setUserNearby(self, user_id, n):
		key = self.client.key(userEnt, user_id)
		if self.client.get(key) == None:
			return 0
		else:
			user = self.client.get(key)	
			user['nearby'] = n
			self.client.put(user)
		return 1

	def userNearby(self, user_id):
		key = self.client.key(userEnt, user_id)
		return self.client.get(key)['nearby']

	def userBuilding(self,user_id):
		parent_key = self.client.key(userEnt, user_id)
		user = self.client.get(parent_key)
		key = self.client.key(userEnt,user_id,logEnt, user['nlogs'])
		return self.client.get(key)['building']

	def listUserLogs(self, user_id):
		ancestor = self.client.key(userEnt, user_id)
		query = self.client.query(kind=logEnt, ancestor=ancestor)
		return list(query.fetch())

	def listUsers(self):
		query = self.client.query(kind=userEnt)
		query.keys_only()
		user_keys = query.fetch()
		users_id = []
		for user in user_keys:
			users_id.append(user.key.name)
		return users_id

	def getUserCoords(self,id):
		log = self.showLog(id)
		return [log['x'],log['y']]

	def usersNearby(self,id):
		coords = self.getUserCoords(id)
		nearby = self.userNearby(id)
		usersNearby = []
		for user in self.listUsers():
			if user != id:
				aux = self.getUserCoords(user)
				r = LA.norm((float(coords[0])-float(aux[0]),float(coords[1])-float(aux[1])))
				if r < nearby:
					usersNearby.append(user)
		return usersNearby
					
#------------------Logs---------------------

	def addLog(self,user_id, x, y, building = 'No building', message =''):
		parent_key = self.client.key(userEnt, user_id)
		user = self.client.get(parent_key)
		user['nlogs'] += 1
		self.client.put(user)

		key = self.client.key(logEnt,user['nlogs'],parent=parent_key)
		log = datastore.Entity(key)
		log.update({
			'building': building,
			'created': datetime.datetime.utcnow(),
			'x': x,
			'y': y,
			'message': message
		})
		self.client.put(log)
		return

	def showLog(self, user_id):
		parent_key = self.client.key(userEnt, user_id)
		user = self.client.get(parent_key)
		key = self.client.key(userEnt,user_id,logEnt, user['nlogs'])
		return self.client.get(key)

	def listAllLogs(self):
		query = self.client.query(kind=logEnt)
		return list(query.fetch())

	def listBuildingLogs(self, building):
		query = self.client.query(kind=logEnt)
		query.add_filter('building', '=', building)
		return list(query.fetch())

#------------------Bots---------------------
	def registerBot(self, name, building, sleep, message):
		key = self.client.key(botEnt,name)
		bot = datastore.Entity(key)
		bot.update({
			'name': name,
			'building': building,
			'sleeptime': sleep,
			'message': message,
			'nmessages' : 0
		})
		self.client.put(bot)

	def checkForBot(self, name):
		key = self.client.key(botEnt,name)
		if self.client.get(key) == None:
			return False
		else:
			return True

	def updateBot(self, name):
		key = self.client.key(botEnt, name)
		bot = self.client.get(key)	
		bot['nmessages'] += 1
		self.client.put(bot)