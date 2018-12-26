from log import *
import pickle


class logDB:
    def __init__(self, name):  
        self.name = name
        try:
            f = open('bd_dumpL' + name, 'rb')
            self.logs = {}
            f.close()
        except IOError:
            self.logs = {}


    def addLog(self,user_id, x, y, building = 'No building'):
        
        try:
            lid = len(self.logs[user_id])
            aux = Log(lid, user_id, x, y, building)
            self.logs[user_id].append(aux)
        except KeyError:
            lid = 1
            aux = []
            aux.append(Log(lid, user_id, x, y, building))
            self.logs[user_id] = aux

        f = open('bd_dumpL' + self.name, 'wb')
        pickle.dump(self.logs, f)
        f.close()

    def showLog(self, user_id):
        return self.logs[user_id][-1]

    def userBuilding(self,user_id):
        return self.logs[user_id][-1].building

    def listAllLogs(self):
        ret = []
        for key in self.logs:
            ret.append(self.logs[key])
        return ret

    def listUserLogs(self, user_id):
        return self.logs[user_id]

    def listUsers(self):
        ret = {}
        i = 1 
        for key in self.logs:
            ret[i] = key 
            i +=1
        return ret

    def listBuildingLogs(self, building):
        ret = []
        for key in self.logs:
            for log in self.logs[key]:
                if log.building == building:
                    ret.append(log)
        return ret
