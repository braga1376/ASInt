from building import *
import pickle


class buildingDB:
    def __init__(self, name):  # PODEMOS RECEBER LOGO A LISTA DE BUILDINGS DO FICHIERO MAYBE?
        self.name = name
        try:
            f = open('bd_dumpB' + name, 'rb')
            #self.builds = pickle.load(f)
            self.builds = {}
            f.close()
        except IOError:
            self.builds = {}

    def addBuilding(self, id, name, x, y):
        #bid = len(self.builds)
        self.builds[id] = Building(id, name, x, y)
        f = open('bd_dumpB' + self.name, 'wb')
        pickle.dump(self.builds, f)
        f.close()


    def showBuilding(self, b_id):
        for b in self.builds:
            if int(b['id']) == b_id:
                return b

    def listAllBuildings(self):
        return list(self.builds.values())


    def listBuildingUsers(self, b_id):
        u = self.builds[b_id].users
        ret = {}
        for i in u:
            ret[i] = 'building ' + b_id
        return ret

    def addUserToBuilding(self, b_id, user_id):
        self.builds[b_id].users.append(user_id)
        return

    def removeUserFromBuilding(self, b_id, user_id):
        self.builds[b_id].users.remove(user_id)
        return
