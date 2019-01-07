#!/usr/bin/env python
# coding=utf-8
from google.cloud import datastore
from numpy import linalg as LA
from geopy.distance import geodesic
import datetime
import json


buildingEnt = 'building'
logEnt = 'log'
userEnt = 'user'
botEnt = 'bot'

class Datastore:
	def __init__(self):
		self.client = datastore.Client.from_service_account_json('credentials.json')

#-------------------General----------------------

	def reset(self):

		entities = ['bot', 'building','user', 'log']

		for entity in entities:
			query = self.client.query(kind=entity)
			query.keys_only()
			resultList = query.fetch()

			for result in resultList:
				self.client.delete(result.key)

		return


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

	def buildingName(self, b_id):
		try:
			key = self.client.key(buildingEnt, b_id)
			building = self.client.get(key)
			ret = building['name']
		except Exception as e:
			return 'No Building'
		return ret

	def listAllBuildings(self):
		query = self.client.query(kind=buildingEnt)
		return list(query.fetch())

	def listBuildingUsers(self, b_id):
		key = self.client.key(buildingEnt, b_id)
		building = self.client.get(key)
		dic={}
		building = self.showBuilding(int(b_id))
		for user in building['users']:
			dic[user] = self.getUserName(user) 					
		return json.dumps(dic)

	def listBuildingUsersID(self, b_id):
		try:
			key = self.client.key(buildingEnt, b_id)
			building = self.client.get(key)
			return building['users']
		except Exception as e:
			return []		
		

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

	def isUserinBuilding(self, x, y, user_id):
		inside = 100
		aux = (x, y)
		possible = []
		mindist = inside
		closer = -1
		for building in self.listAllBuildings():
			build = float(building['x']), float(building['y'])
			r = geodesic(build, aux).meters
			if r < inside and r < mindist:
				closer = building.key.id

		if closer != -1:
			return closer
		else:
			return 0

#------------------User---------------------
	
	def addUser(self, user_id, name):
		key = self.client.key(userEnt, user_id)
		if self.client.get(key) == None:
			user = datastore.Entity(key)
			user['name'] = name
			user['nlogs'] = 0
			user['nearby'] = 1000
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
		try:
			key = self.client.key(userEnt, user_id)
			if self.client.get(key) == None:
				return 0
			else:
				user = self.client.get(key)	
				return user['token']
		except Exception as e:
			return 0
		

	def setUserNearby(self, user_id, n):
		try:
			key = self.client.key(userEnt, user_id)
			if self.client.get(key) == None:
				return 0
			else:
				user = self.client.get(key)	
				user['nearby'] = int(n)
				self.client.put(user)
			return 1			
		except Exception as e:
			return 0

	def userNearby(self, user_id):
		try:
			key = self.client.key(userEnt, user_id)
			return self.client.get(key)['nearby']
		except Exception as e:
			return 0

	def userBuilding(self,user_id):
		try:
			parent_key = self.client.key(userEnt, user_id)
			user = self.client.get(parent_key)
			key = self.client.key(userEnt,user_id,logEnt, user['nlogs'])
			return self.client.get(key)['building']
		except Exception as e:
			return 0
		

	def listUserLogs(self, user_id):
		ancestor = self.client.key(userEnt, user_id)
		query = self.client.query(kind=logEnt, ancestor=ancestor)
		return list(query.fetch())

	def listUsers(self):
		query = self.client.query(kind=userEnt)
		user_keys = query.fetch()
		users= {}
		for user in user_keys:
			users[user.key.name] = user['name']
		return json.dumps(users,sort_keys=True, ensure_ascii=False)

	def getUserCoords(self,id):
		try:
			log = self.showLog(id)
			res = [log['x'],log['y']]
		except Exception as e:
			return None
		return res

	def getUserName(self,id):
		key = self.client.key(userEnt, id)
		user = self.client.get(key)
		return user['name']

	def usersNearby(self,id):
		try:
			c = self.getUserCoords(id)
			coords = (c[0],c[1])
			nearby = self.userNearby(id)
			dic={}
			users = json.loads(self.listUsers())
		except:
			return {}
		for user in users:
			if user != id:
				try:
					c = self.getUserCoords(user)
					aux = (c[0],c[1])
					r = geodesic(coords, aux).meters
					name = users[user]
					if r < nearby:
						dic[user] = name
				except Exception as e:
					pass
					
		return json.dumps(dic)

	def usersNearbyID(self,id):
		try:
			c = self.getUserCoords(id)
			coords = (c[0],c[1])
			nearby = self.userNearby(id)
			users = []
			for user in json.loads(self.listUsers()):
				if user != id:
					try:
						c = self.getUserCoords(user)
						aux = (c[0],c[1])
						r = geodesic(coords, aux).meters
						if r < nearby:
							users.append(user) 
					except Exception as e:
						pass
			return users
		except Exception as e:
			return []
		
					
#------------------Logs---------------------

	def addLog(self, user_id, x, y, building=0, message={}):
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
			'data': message
		})
		self.client.put(log)
		return

	def showLog(self, user_id):
		parent_key = self.client.key(userEnt, user_id)
		try:
			user = self.client.get(parent_key)
					
			key = self.client.key(userEnt,user_id,logEnt, user['nlogs'])
		
			result =  self.client.get(key)
		except Exception as e:
			return None		
		return result

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