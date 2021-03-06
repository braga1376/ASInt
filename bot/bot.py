#coding=utf-8
import requests
import json
import copy
import time


class Bot:
	
	def __init__(self, host, data, sleep):		
		self.host = host
		self.data = data 
		self.sleep = sleep

	def sendMessage(self):
		requests.post(self.host + '/API/Bots/SendMessage', data = self.data)

def dataToDict(name, bid, message, sleep):
	d = {}
	d['name'] = '[BOT]-'+name
	d['bid'] = bid
	d['message'] =message
	d['sleeptime'] = sleep
	data = json.dumps(d)
	return(data)

def main():
	
	host = 'http://127.0.0.1:5000'
	#host = 'https://asint-project-2018.appspot.com'

	print('----Lets create a Bot!----')
	print('Please insert Bot\'s name')
	name = input("\n> ")
	print('Please insert Bot\'s Building id (int)')
	bid = int(input("\n> "))
	print('What message should the Bot send?')
	message = input("\n> ")
	print('What\'s the Sleeping period?(seconds)')
	sleep = int(input("\n> "))

	data = dataToDict(name, bid, message, sleep)
	bot = Bot(host, data, sleep)

	#bot = Bot(host, 1, 4, 'hello im bot', 30)
	i = 1
	#bot.sendMessage()
	while(True):
		bot.sendMessage()
		time.sleep(sleep)
		print('sent message'+ str(i))
		i+=1

if __name__ == "__main__":
	main()