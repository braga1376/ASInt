from google.cloud import datastore

buildingEnt = 'building'
logEnt = 'log'
userEnt = 'user'

class Datastore:
	def __init__(self):
		self.client = datastore.Client.from_service_account_json('ASInt-977d919195b1.json')

#------------------Buildings---------------------

	def addBuilding(self, id, name, x, y):
		key = self.client.key(buildingEnt, id)
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


#------------------Logs---------------------
	
	def addUser(self, user_id):
		key = self.client.key(userEnt, user_id)
		user = datastore.Entity(key)
		user['nlogs'] = 0
		user['nearby'] = 10
		self.client.put(user)
		return

	def addLog(self,user_id, x, y, building = 'No building', message =''):
		parent_key = self.client.key(userEnt, user_id)
		user = self.client.get(parent_key)
		user['nlogs'] += 1
		#ADD NEARBY
		self.client.put(user)

		key = self.client.key(logEnt,user['nlogs'],parent=parent_key)
		log = datastore.Entity(key)
		log.update({
			'building': building,
			'x': x,
			'y': y,
			'message': message
		})
		self.client.put(log)
		return

	def showLog(self, user_id):
		parent_key = self.client.key(userEnt, user_id)
		user = self.client.get(parent_key)
		key = client.key(logEnt, user['nlogs'])
		return self.client.get(key)

	def userBuilding(self,user_id):
		parent_key = self.client.key(userEnt, user_id)
		user = self.client.get(parent_key)
		key = client.key(logEnt, user['nlogs'])
		return self.client.get(key)['building']

	def listAllLogs(self):
		query = self.client.query(kind=logEnt)
		return list(query.fetch())

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

	def listBuildingLogs(self, building):
		query = self.client.query(kind=logEnt)
		query.add_filter('building', '=', building)
		return list(query.fetch())