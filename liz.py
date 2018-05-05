#!/usr/bin/env python
import sys
import click
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from pyshorteners import Shortener
import requests
import speedtest

st = speedtest.Speedtest()
stop_words = set(stopwords.words('english'))
stop = ["stop listening","sleep","stop functioning", "exit", "shutdown", "shut down", "power off","stop","off","close"]
yes = ['At once sir','Sure','On it','Alright sir']
api_key_url = 'AIzaSyDJDbHcXB-tC9nm5kZGy-i9Vc-AgXXIApI'
shortener = Shortener('Google', api_key=api_key_url)
url_start = "https://"
@click.command()
def main():
	command=""
	print "Yes sir?"
	while(command.lower() not in stop):
		command = raw_input('> ')
		word_tokens = word_tokenize(command)
		command_words = [w for w in word_tokens if not w in stop_words]
		if command not in stop:
			print random.choice(yes)
			for i in command_words:

				#shorten_url
				if i in ['shorten','short','small','smaller']:
					flag=0
					for i in command_words:
						try:
							url = 'http://'+i
							print "\rThe shortened url is {}".format(shortener.short(url))
							flag=1
						except :
							pass
					if flag==0:
						print "Sorry sir, cannot shorten this url"
					continue

				#expand_url
				if i in ['expand','enlarge','big','large']:
					flag=0
					for i in command_words:
						try:
							url = i
							if url_start in url:
								print "The expanded url is {}".format(shortener.expand(url))
							else:
								url = url_start+i
								print "The expanded url is {}".format(shortener.expand(url))
							flag=1
						except :
							pass

					if flag==0:
						print "Sorry sir, cannot expand this url"

				#speedtest
				if i in ['server','speed','network','connection','download','upload','ping','speedtest']:
					print "BEST SERVER: " + st.get_best_server()['url'] 
					print "DOWNLOAD: " + str(st.download()/(1024*1024)) + " MBPS"
					print "UPLOAD: " + str(st.upload()/(1024*1024)) +  " MBPS"



			print "\nWhat would you like me to do?"
		
	if command.lower() in stop:
		print "I'll not be listening now\n"

if __name__=='__main__':
	main()