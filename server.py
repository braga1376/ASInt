from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import json
from buildingDB import *
from logDB import *


app = Flask(__name__)
BuildsDB = buildingDB("builds")
LogsDB = logDB("logs")


@app.route('/')
def mainpage():
    return render_template("mainPage.html")

#------------------ADMIN---------------------

@app.route('/API/Admin/Buildings', methods = ['POST'])
def receiveBuildings():#receive all buildings fromm admin and send them to DB

    data=json.loads(request.data)
    
    for b in data:
        bid = b['id']
        name = b['name']
        x = b['x']
        y = b['y']
        BuildsDB.addBuilding(bid, name, x, y)

    builds = BuildsDB.listAllBuildings()
    bdict = list(map(lambda x: x.to_dict(), builds))
    return jsonify(bdict)
    
@app.route('/API/Admin/Users')
def sendUsers(): #list all users
    users = LogsDB.listUsers()
    return jsonify(users)   

@app.route('/API/Admin/Buildings/<id>/Users')
def usersOnBuilding(id): #list all users from a building
    users = BuildsDB.listBuildingUsers(id)
    return jsonify(users)

@app.route('/API/Admin/Logs/Users/<id>', methods = ["GET"])
def userHistory(id): #returns user logs history
    logs = LogsDB.listUserLogs(id)
    logsdict = list(map(lambda x: x.to_dict(), logs))
    return jsonify(logsdict)

@app.route('/API/Admin/Logs/Buildings/<id>')
def buildingHistory(id): #returns building logs history
    logs = LogsDB.listBuildingLogs(id)
    logsdict = list(map(lambda x: x.to_dict(), logs))
    return jsonify(logsdict)

#------------------USERS---------------------

@app.route('/API/Users')
def userMainPage():
    return render_template("UserMainPage.html")


@app.route('/API/Users/Location', methods = ["GET"])
def userLocation():#receive user location
    if request.args["UserID"] == None:
        pass
    else:
        userid = request.args["UserID"]
    if request.args["x"] == None:
        pass
    else:
        xx = request.args["x"]
    if request.args["y"] == None:
        pass
    else:
        yy = request.args["y"]
    if request.args["building"] == None or request.args["building"] == '':#não vai estar cá, só para teste
        LogsDB.addLog(userid, xx, yy)     #em vez disto é calcular o build com as coords
    else:
        bid = request.args["building"]
        try:
            if LogsDB.userBuilding(userid) != bid:
                BuildsDB.removeUserFromBuilding(LogsDB.userBuilding(userid), userid)
        except Exception as e:
            pass
        LogsDB.addLog(userid, xx, yy,building = bid)
       
        try:
            BuildsDB.addUserToBuilding(bid,userid)
        except Exception as e:
            pass

    #check if in anybuilding
    #if (xx && yy) in buildings :
    #    building = BUILDING NAME
    
    logs = LogsDB.listAllLogs()
    
    return render_template("UserMainPage.html")

@app.route('/API/Users/<id>/Message')
def userMessage():
    pass

@app.route('/API/Users/<id>/Setnearby')
def setNearby():#(?)
    pass

@app.route('/API/Users/<id>/Nearby')
def usersNearby():
    pass

#------------------BOTS----------------------

@app.route('/API/Bots/Register')
def register():
    pass

@app.route('/API/Bots/Message')
def botMessage():
    pass