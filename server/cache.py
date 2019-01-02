import os
import bmemcached

class Cache:
	def __init__(self):
		# Environment variables are defined in app.yaml.
		MEMCACHE_SERVER = os.environ.get('MEMCACHE_SERVER', 'localhost:11211')
		MEMCACHE_USERNAME = os.environ.get('MEMCACHE_USERNAME')
		MEMCACHE_PASSWORD = os.environ.get('MEMCACHE_PASSWORD')

		self.memcache_client = bmemcached.Client([MEMCACHE_SERVER], MEMCACHE_USERNAME, MEMCACHE_PASSWORD)

	def insert(self, username, secret, time = None):
		if time == None:
			self.memcache_client.set(username, secret)
		else:
			self.memcache_client.set(username, secret, time = time)

	def check(self, username):

		print(self.memcache_client.get(username))
		if self.memcache_client.get(username) != None:
			return True
		else:
			return False