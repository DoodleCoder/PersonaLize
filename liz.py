#!/usr/bin/env python
import sys
import click
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from pyshorteners import Shortener
import requests
import speedtest
import json
import urllib2
import math
import re
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep
from googlesearch.googlesearch import GoogleSearch as gs
import calendar
from datetime import datetime as dt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import getpass
import sqlite3
import chalk


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


CLIENT_ACCESS_TOKEN_APIAI = 'd9a374098afd43a9828fc039c34ab5f2'
st = speedtest.Speedtest()
stop_words = set(stopwords.words('english'))
stop = ["stop listening","sleep","stop functioning", "bye", "exit", "shutdown", "shut down", "power off","stop","off","close"]
yes = ['At once sir','Sure','On it','Alright sir']
api_key_url = 'AIzaSyDJDbHcXB-tC9nm5kZGy-i9Vc-AgXXIApI'
shortener = Shortener('Google', api_key=api_key_url)
url_start = "https://"
fallback = ["I didn't get that. Can you say it again?","I missed what you said. Say it again?","Sorry, could you say that again?","Sorry, can you say that again?","Can you say that again?","Sorry, I didn't get that.","Sorry, what was that?","One more time?","What was that?","Say that again?","I didn't get that.","I missed that."]


@click.command()
def main():
	command=""
	print chalk.blue("Yes sir?")
	while 1:
		if command.lower() in stop:
			break
		else:
			global reply 
			reply = ""
			print chalk.cyan("\nWhat would you like me to do?")
			command = raw_input('> ')
			try:
				ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN_APIAI)
				requestai = ai.text_request()
				requestai.lang = 'en' 
				requestai.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
				requestai.query = command
				response = requestai.getresponse()
				reply0 = json.loads(response.read())
				reply1 = reply0['result']['fulfillment']['messages']
				reply = reply1[0]['speech']
			except :
				pass
			if reply in fallback:
				word_tokens = word_tokenize(command)
				command_words = [w for w in word_tokens if not w in stop_words]
				if command not in stop:
					for i in command_words:

                        #shorten_url
						if i in ['shorten','short','small','smaller']:
							flag=0
							print chalk.yellow(random.choice(yes))
							for i in command_words:
								try:
									url = 'http://'+i
									reply = "\rThe shortened url is {}".format(shortener.short(url))
									print chalk.green(reply)
									flag=1
								except :
									pass
							
							if flag==0:
								reply = "Sorry sir, cannot shorten this url"
								print chalk.red(reply)
							reply=''
							break

                        #expand_url
						elif i in ['expand','enlarge','big','large']:
							flag=0
							print chalk.yellow(random.choice(yes))
							for i in command_words:
								try:
									url = i
									if url_start in url:
										reply = "The expanded url is {}".format(shortener.expand(url))
									else:
										url = url_start+i
										reply = "The expanded url is {}".format(shortener.expand(url))
									flag=1
									print chalk.green(reply)
				
								except :
									pass

							if flag==0:
								reply = "Sorry sir, cannot expand this url"
								print chalk.red(reply)

							reply = ''
							break

                        #speedtest
						elif i in ['server','speed','network','connection','download','upload','ping','speedtest']:
							print chalk.yellow(random.choice(yes))
							reply =  "BEST SERVER: " + st.get_best_server()['url'] + "\nDOWNLOAD: " + str(st.download()/(1024*1024)) + " MBPS\nUPLOAD: " + str(st.upload()/(1024*1024)) +  " MBPS"
							print chalk.green(reply)
							reply = ''
							break
						
						#calendar
						elif i in ['datetime','date','month','calendar','year','time']:
							print chalk.yellow(random.choice(yes))
							y=dt.now().year
							m=dt.now().month
							d=dt.now().day	
							c = calendar.TextCalendar(calendar.SUNDAY)
							cal = c.formatmonth(y, m)
							print chalk.blue(cal)
							hour = dt.now().hour
							half = ' AM'
							if hour > 12:
								hour -= 12
								half = ' PM'
							minute = dt.now().minute
							if minute < 10:
								minute = "0"+str(minute)
							time = str(hour)+":"+ str(minute) + half
							print chalk.green("NOW : ")
							reply = str(d)+"/"+str(m)+"/"+str(y)+" - "+ time
							print chalk.green(reply)
							reply =''
							break

						#email
						elif i in ['mail','email','attach','electronic-mail']:
							print chalk.yellow(random.choice(yes))
							fromaddr = raw_input("~Enter Your Email Address: ")
							pas = getpass.getpass()
							toaddr = raw_input("~Enter Reciever's Email Address: ")							 
							msg = MIMEMultipart()
							msg['From'] = fromaddr
							msg['To'] = toaddr
							msg['Subject'] = raw_input("~Enter the subject of the mail: ")	
							body = raw_input("~Enter the body of the mail: ")
							part1 = MIMEText(body,'plain')
							msg.attach(MIMEText(body, 'plain'))
							choice = raw_input("~Enter 1 to make an attachment: ")
							if choice == "1":
								filename = raw_input("~Enter the name of the attachment: ")
								path_to_file = raw_input("~Enter the path to the attachment: ")
								attachment = open(path_to_file, "rb")
								part = MIMEBase('application', 'octet-stream')
								part.set_payload((attachment).read())
								encoders.encode_base64(part)
								part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
								msg.attach(part)					 
							server = smtplib.SMTP('smtp.gmail.com', 587)
							server.starttls()
							server.login(fromaddr, pas)
							text = msg.as_string()
							server.sendmail(fromaddr, toaddr, text)
							server.quit()
							print chalk.green("Mail successfully sent!")
							reply=""
							break

						#weather
						elif i in ['weather','weathers','condition','temperature','hot','cold']:
							print chalk.yellow(random.choice(yes))
							try:
								place = command.split(i+" of ")[1] #raw_input('~Enter the name of city: ')
							except:
								place = command.split(i)[1]
							if place == '':
								place = raw_input('~Enter the name of the city: ')
							r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+place+'&APPID=eaa27a7b42b031a60e68312e9a689569')
							a = r.json()
							temp = str(int(a['main']['temp']) - 273)
							print chalk.green("Weather conditions of "+place+" is: " + a['weather'][0]['description'] + "\nTemperature: " + temp + "\nHumidity: " + str(a['main']['humidity']) +  "\nPressure : "+str(a['main']['pressure']) + "\nWind : " + str(a['wind']['speed']))
							reply = ""
							break

						#diary
						elif i in ['note down','write down','jot down','jot','write','note','diary']:
							print chalk.yellow(random.choice(yes))
							db = sqlite3.connect('diary.db')
							c = db.cursor()
							try:
								c.execute(''' CREATE TABLE note(id INTEGER PRIMARY KEY, d TEXT, t TEXT, entry TEXT)
								''')
								db.commit()
							except:
								pass
							c = db.cursor()
							day = dt.now().day
							month = dt.now().month
							year = dt.now().year
							dateNote = str(day)+"/"+str(month)+"/"+str(year)
							hourNote = dt.now().hour
							half = ' AM'
							if hourNote > 12:
								hourNote -= 12
								half = ' PM'
							minuteNote = dt.now().minute
							if minuteNote < 10:
								minuteNote = "0"+str(minuteNote)
							timeNote = str(hourNote)+":"+ str(minuteNote) + half
							textNote = str(raw_input("What should I note down sir? "))
							c.execute(''' INSERT INTO note(d, t, entry)
                  					VALUES(?,?,?) ''', (dateNote, timeNote, textNote))
							db.commit()
							print chalk.green('Sucessfully noted down sir!')
							ch = raw_input('~Enter 1 to view all notes: ')
							if ch == '1':
								c.execute('''SELECT * FROM note ORDER BY d,t''')
								allNotes = c.fetchall()
								print chalk.yellow("Date \t\tTime \t\tText")
								for i in allNotes:
									print chalk.blue(str(i[1])+" \t"+str(i[2])+" \t"+str(i[3]))
							reply=""
							break

						#wallet
						elif i in ['wallet','transaction','money','balance']:
							print chalk.yellow(random.choice(yes))
							db2 = sqlite3.connect('wallet.db')
							c = db2.cursor()
							try:
								c.execute(''' CREATE TABLE wallet(id INTEGER PRIMARY KEY, d TEXT, details TEXT,  type TEXT, amount INTEGER, balance INTEGER)
								''')
								c = db2.cursor()
								date0 = '05/05/2018'
								detail0 = 'Open'
								type0 = 'O'
								amount = 0
								balance = 0
								c.execute(''' INSERT INTO wallet(details, d, type, amount, balance)
								              VALUES(?,?,?,?,?) ''', (detail0,date0,type0,amount,balance))
								db2.commit()
							except:
								pass

							if command in ['show balance','display balance','money left','balance','wallet','wallet balance']:
								c.execute("SELECT * FROM wallet ORDER BY id DESC LIMIT 1")
								result = c.fetchone()
								balance = result[5]
								print chalk.green("Current Balance is : " + str(balance))
								ch2 = raw_input('Enter 1 to view wallet transactions: ')
								if ch2 =='1':
									c.execute('''SELECT * FROM wallet''')
									allTx = c.fetchall()
									print chalk.yellow("ID \tDate \t\tDetails \tType \tAmount \tBalance")
									for i in allTx:
										print chalk.blue(str(i[0])+" \t"+str(i[1])+" \t"+str(i[2])+" \t\t"+str(i[3])+" \t"+str(i[4])+" \t"+str(i[5]))
								reply = ''
								break
							else:
								c = db2.cursor()
								print chalk.white("------------Transaction Details------------")
								date1 = raw_input('~Enter the date (dd/mm/yyyy) : ')
								detail1 = raw_input('~Enter the details : ')
								type1 = raw_input('~Enter C/D for Credit/Debit : ')
								while type1 not in ['C','D']:
									print "Wrong input"
									type1 = raw_input('~Enter C/D for Credit/Debit : ')	
								amount1 = int(raw_input('~Enter the amount : '))
								c.execute("SELECT * FROM wallet ORDER BY id DESC LIMIT 1")
								result = c.fetchone()
								balance = result[5]
								if type1 == 'C':
									balance+=amount1
								else:
									balance-=amount1
								c.execute(''' INSERT INTO wallet(details, d, type, amount, balance)
								              VALUES(?,?,?,?,?) ''', (detail1,date1,type1,amount1,balance))
								db2.commit()
								print "-------------------------------------------"
							ch2 = raw_input('Enter 1 to view wallet transactions: ')
							if ch2 =='1':
									c.execute('''SELECT * FROM wallet''')
									allTx = c.fetchall()
									print chalk.yellow("ID \tDate \t\tDetails \tType \tAmount \tBalance")
									for i in allTx:
										print chalk.blue(str(i[0])+" \t"+str(i[1])+" \t"+str(i[2])+" \t\t"+str(i[3])+" \t"+str(i[4])+" \t"+str(i[5]))
							reply = ''
							break

						#googlesearch
						elif i in ['google','search','look up','find']:
							print chalk.yellow(random.choice(yes))
							w = command.split(i+" ")
							word = w[1]
							try:
								resp = gs().search(word)
								allr = resp.results
								i=1
								if len(allr) > 10:
									allr = allr[:10]
								for r in allr:
									print  chalk.blue(str(i) + ". " + r.title + " - " + r.url) 								
									i+=1
								reply="There are " + str(i-1) + " matching results"
								print chalk.green(reply)
								reply = ''
							except:
								pass

			print chalk.red(reply)
			reply = ""

	if command.lower() in stop:
		print chalk.blue("I'll not be listening now\n")

if __name__=='__main__':
	main()