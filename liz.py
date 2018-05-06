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
stop = ["stop listening","sleep","stop functioning", "exit", "shutdown", "shut down", "power off","stop","off","close"]
yes = ['At once sir','Sure','On it','Alright sir']
api_key_url = 'AIzaSyDJDbHcXB-tC9nm5kZGy-i9Vc-AgXXIApI'
shortener = Shortener('Google', api_key=api_key_url)
url_start = "https://"
fallback = ["I didn't get that. Can you say it again?","I missed what you said. Say it again?","Sorry, could you say that again?","Sorry, can you say that again?","Can you say that again?","Sorry, I didn't get that.","Sorry, what was that?","One more time?","What was that?","Say that again?","I didn't get that.","I missed that."]


@click.command()
def main():
	command=""
	print "Yes sir?"
	while 1:
		if command.lower() in stop:
			break
		else:
			global reply 
			reply = ""
			print "\nWhat would you like me to do?"
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
							print random.choice(yes)
							for i in command_words:
								try:
									url = 'http://'+i
									reply = "\rThe shortened url is {}".format(shortener.short(url))
									flag=1
								except :
									pass
							if flag==0:
								reply = "Sorry sir, cannot shorten this url"
							continue

                        #expand_url
						elif i in ['expand','enlarge','big','large']:
							flag=0
							print random.choice(yes)
							for i in command_words:
								try:
									url = i
									if url_start in url:
										reply = "The expanded url is {}".format(shortener.expand(url))
									else:
										url = url_start+i
										reply = "The expanded url is {}".format(shortener.expand(url))
									flag=1
				
								except :
									pass

							if flag==0:
								reply = "Sorry sir, cannot expand this url"

                        #speedtest
						elif i in ['server','speed','network','connection','download','upload','ping','speedtest']:
							print random.choice(yes)
							reply =  "BEST SERVER: " + st.get_best_server()['url'] + "\nDOWNLOAD: " + str(st.download()/(1024*1024)) + " MBPS\nUPLOAD: " + str(st.upload()/(1024*1024)) +  " MBPS"
						
						#googlesearch
						elif i in ['google','search','look up','find']:
							print random.choice(yes)
							w = command.split(i+" ")
							word = w[1]
							resp = gs().search(word)
							allr = resp.results
							i=1
							if len(allr) > 10:
								allr = allr[:10]
							for r in allr:
								print  str(i) + ". " + r.title + " - " + r.url 								
								i+=1
							reply="There are " + str(i-1) + " matching results"
			print reply
			reply = ""

	if command.lower() in stop:
		print "I'll not be listening now\n"

if __name__=='__main__':
	main()