#coding=utf-8
import requests
import json
import copy
import sys
import getpass


class Admin:

    def __init__(self, host):
        self.host = host
        self.nbuilds = 0

    def getFromURI(self, uri):# receive values from request
        r = requests.get(self.host + uri)
        #print(r)
        data = r.json()
        return(data)

    def getURI(self, uri):# receive values from request
        r = requests.get(self.host + uri)

    def postToURI(self, uri, d):
        r = requests.post(self.host + uri, data = d )
        #print(r.text)
        return r.text

    def readFileToJSon(self, f):
        d = {}
        dic = []
        print('Buildings Sent:')
        for line in f:
            s = line.replace('\n','').split(' ')
            d['id'] = s[0]
            d['name'] = s[1].replace('_', ' ')
            print('->'+d['name'])
            d['x'] = s[2]
            d['y'] = s[3]
            dic.append((copy.deepcopy(d)))
            self.nbuilds +=1
        return json.dumps(dic)
            

    def menu(self):#

        #g = geocoder.ip('me')
        #print(g.latlng)
        while (1):
            print(
                '\nCommands available:\n\t1 - DEFINE BUILDINGS '
                '\n\t2 - LIST USERS  \n\t3 - LIST USERS IN A BUILDING '
                '\n\t4 - USER LOGS\n\t5 - RESET DATABASE\n\t6 - EXIT')
            command = input("\n> ")
            if (command == "1"):
                file = open('buildings',"r", encoding = "utf-8-sig")
                j = self.readFileToJSon(file)
                #print(j)
                uri = '/API/Admin/Buildings'
                data = self.postToURI(uri, j)

            elif (command == "2"):
                uri = '/API/Admin/Users'
                data = self.getFromURI(uri)
                for key in data.keys():
                    print(key+'->'+data[key])

            elif (command == "3"):
                buildingid = input("\n\tBuilding Identifier:\n\t\t")
                if int(buildingid) < 1 or (buildingid) > nbuilds:
                    print('There is no such building, sorry!')
                    continue
                uri = '/API/Admin/Buildings/' + buildingid + '/Users'
                data = self.getFromURI(uri)
                for key in data.keys():
                    print(key+'->'+data[key])

            elif (command == "4"):
                userid = input("\n\tUser Identifier:\n\t\t")
                uri = '/API/Admin/Logs/Users/' + userid
                data = self.getFromURI(uri)                
                for item in data:
                    if item['data'] == {}: 
                        string = f"{item['created']}, building: {item['building']}, coords: ({item['x']},{item['y']})"
                    else:
                        string = f"{item['created']}, building: {item['building']}, coords: ({item['x']},{item['y']}), Message: {item['data']['message']} From {item['data']['sender']}"
                    print(string)
#item['created'] + '\tbuilding: ' + item['building']+ '\tcoords ' +
            elif (command == "5"):
                uri = '/API/Admin/ResetDB'
                print("Performing Reset...")
                self.getURI(uri)
                print("Reset Complete!")

            elif (command == "6"):
                return

            else:
                print("'%s' is not a valid command" % (command))

def main():
    
    user = getpass.getuser()

    #admin = Admin('https://asint-226517.appspot.com')
    #admin = Admin('http://127.0.0.1:5000')
    admin = Admin('https://asint-project-2018.appspot.com')
    for x in range (0,3):
        pswd = getpass.getpass('Password:')
        admind = {'admin':user,'pswd':pswd}
        uri = '/API/Admin'
        #print(json.dumps(admind))
        if admin.postToURI(uri, json.dumps(admind)) == "true":
            print('Successful Login!')
            break
        else:
            if x == 2:
                return
            else:
                print('Invalid Admin User or Password')
    
    admin.menu()

if __name__ == "__main__":
    main()