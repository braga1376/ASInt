#!/usr/bin/env python
# coding=utf-8
import os
import json
import fenixedu
from flask import Flask, render_template, request, jsonify, redirect

from cache import *
from datastore import *
from messages import *

app = Flask(__name__)

datastore = Datastore()

cache = Cache()

admins = {'francisco':'123','miguel':'123'}

messages = Messages(datastore)

@app.route('/')
def mainpage():
	return render_template("mainPage.html", data = datastore.listAllBuildings())

#------------------ADMIN---------------------

@app.route('/API/Admin', methods = ['POST'])
def adminLogin(): #receive and verify user and password of admin
	data=json.loads(request.data)

	admin = data['admin']
	pswd = data['pswd']

	try:
		if admins[admin] == pswd:
			return "true"
	except Exception as e:
		pass
		
	return "false"

@app.route('/API/Admin/Buildings', methods = ['POST'])
def receiveBuildings():#receive all buildings fromm admin and send them to DB

	data=json.loads(request.data)
	
	for b in data:
		bid = b['id']
		name = b['name']
		x = b['x']
		y = b['y']
		datastore.addBuilding(bid, name, float(x), float(y))

	builds = datastore.listAllBuildings()
	return jsonify(builds)
	
@app.route('/API/Admin/Users')
def sendUsers(): #list all users
	return datastore.listUsers()

@app.route('/API/Admin/Buildings/<id>/Users')
def usersInBuilding(id): #list all users from a building
	return  datastore.listBuildingUsers(id)

@app.route('/API/Admin/Logs/Users/<id>', methods = ["GET"])
def userHistory(id): #returns user logs history
	logs = datastore.listUserLogs(id)
	#logsdict = list(map(lambda x: x.to_dict(), logs))
	return jsonify(logs)

@app.route('/API/Admin/Logs/Buildings/<id>')
def buildingHistory(id): #returns building logs history
	logs = datastore.listBuildingLogs(id)
	return jsonify(logs)

@app.route('/API/Admin/ResetDB')
def resetDB(): #resets Database
	datastore.reset()
	return "OK"

#------------------USERS---------------------

@app.route('/API/Users/Login')
def userLogin():
	config = fenixedu.FenixEduConfiguration.fromConfigFile()
	client = fenixedu.FenixEduClient(config)
	url = client.get_authentication_url()
	return redirect(url)

@app.route('/API/Users/Home', methods = ["GET"])
def userMainPage():
	if request.args["code"] == None:
		pass
	else:
		try:
			code = request.args["code"]
			config = fenixedu.FenixEduConfiguration.fromConfigFile()
			client = fenixedu.FenixEduClient(config)
			user = client.get_user_by_code(code)
			person = client.get_person(user)
			cache.insert(person['username'], code, 60*60)
			datastore.addUser(person['username'], person['name'])
		except Exception as e:
			return redirect("/API/Users/Login")
	
	return render_template("UserMainPage.html", username = person['username'])

@app.route('/API/Users/SendLog', methods = ["GET"])
def userLog():#receive user location
	if request.args["UserID"] == None:
		return "Not OK"
	else:
		userid = request.args["UserID"]
		if not cache.check(userid):
			return "TIMEOUT"
	if request.args["x"] == None:
		return "Not OK"
	else:
		xx = request.args["x"]
	if request.args["y"] == None:
		return "Not OK"
	else:
		yy = request.args["y"]
	if(xx == 'undefined' or yy == 'undefined'):
		return "LOCUNDEFINED"
	else:
		bid = datastore.isUserinBuilding(xx,yy,userid)
		try:
			if datastore.userBuilding(userid) != bid:
				datastore.removeUserFromBuilding(datastore.userBuilding(userid), userid)
		except Exception as e:
			pass
		datastore.addLog(userid, xx, yy,building = bid)
		try:
			datastore.addUserToBuilding(bid,userid)
		except Exception as e:
			pass
			
	return "OK"

@app.route('/API/Users/<id>/MyBuilding', methods = ["GET"])
def myBuildind(id):
	bid = datastore.userBuilding(id)
	return datastore.buildingName(bid)

	

@app.route('/API/Users/<id>/SetToken', methods = ["GET"])
def setUserToken(id):
	if not cache.check(id):
			return "TIMEOUT"
	if request.args["token"] == None:
		return "Not OK"
	else:
		utoken = request.args["token"]    
	if datastore.setUserToken(id, utoken) == 0:
		return "Not OK"
	return "OK"

@app.route('/API/Users/<id>/MessageBuilding', methods = ["POST"])
def userMessageBuilding(id):
	data = json.loads(request.data.decode())
	bid = datastore.userBuilding(id)    
	messages.sendToBuilding(data, id, bid)
	return "OK"

@app.route('/API/Users/<id>/MessageNearby', methods = ["POST"])
def userMessageNearby(id):
	data = json.loads(request.data.decode())
	messages.sendToNearby(data, id)    
	return "OK"

@app.route('/API/Users/<id>/SetNearby/<n>', methods = ["GET"])
def setNearby(id,n):
	datastore.setUserNearby(id, n)
	return "OK"

@app.route('/API/Users/<id>/SetNearby/', methods = ["GET"])
def setNearbyEmpty(id,n):
	pass

@app.route('/API/Users/<id>/Nearby')
def usersNearby(id):
	try:
		ret = datastore.usersNearby(id)
	except Exception as e:
		return {}
	return ret

#------------------BOTS----------------------

@app.route('/API/Bots/SendMessage', methods = ['POST'])
def botMessage():
	data = {}
	bot = json.loads(request.data)
	bid = int(bot['bid'])
	name = bot['name']
	data['message'] = bot['message']
	sleep = int(bot['sleeptime'])
	
	# if not in datastore, register
	if not datastore.checkForBot(name):
		datastore.registerBot(name, bid, sleep, data)
	
	messages.sendToBuilding(data, name, bid, bot = 1)
	datastore.updateBot(name)

	return "OK"
	

##--------------Serviceworker----------------

@app.route('/firebase-messaging-sw.js', methods=['GET'])
def sw():
	return app.send_static_file('firebase-messaging-sw.js')

if __name__ == '__main__':
	app.run(host = '127.0.0.1', port = 5000, debug = True)