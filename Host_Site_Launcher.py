#Class: 18-549 Celloc
#Author: Justin Wang - jwwang
#Group: group 21

from apiclient.discovery import build

import re
import sys
import googlemaps
import urllib
import urllib2
import json
import httplib2
import pickle
import webbrowser

from googlemaps import GoogleMapsError
from googlemaps import GoogleMaps
from apiclient.oauth import FlowThreeLegged
from apiclient.ext.authtools import run
from apiclient.ext.file import Storage


def YoutubeLink(content):
	content = content.replace(' ', '+')
	urlstring = "http://www.youtube.com/results?search_query=" + content
	page = urllib.urlopen(urlstring)
	source = page.read()
	if source.find("No video results for"):
		print "No video results found for " + content
		return
	firstLinkIndex = source.find("watch?v=")
	source = source[firstLinkIndex:]
	firstLinkEnd = source.find("class")
	source = source[:firstLinkEnd]
	videoID = source[:-2]
	videoURL = "http://www.youtube.com/" + videoID
	webbrowser.open(videoURL)
	return

def GoogleMapAddress(destination):
#	gmaps = GoogleMaps()
	#for now assume getLocation returns a latitude/longitude string
	#in format "latitude longitude"
	address = getLocation()
#	print "Driving Directions from: " + address
#	print "                   to: " + destination
#	try:
#		directions = gmaps.directions(address, destination)
#	except GoogleMapsError:
#		print "An error has been raised, likely needs specific address"
#		return
#	createHTML(directions)
	mapsURL = 'http://maps.google.com/maps?saddr='+address+'&daddr='+destination
	webbrowser.open(mapsURL)
#	for step in directions['Directions']['Routes'][0]['Steps']:
#		p = re.compile(r'<.*?>')	
#		item = step['descriptionHtml']
#		item = p.sub(' ', item)		
#		print item
	return

#def createHTML(directions):
#	f = open('directionsPage.html', 'w')
#	f.write('<html><head><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><title>Google Maps Directions</title></head><body><img src="GmapsLogo.jpg"/><br>')
#	for step in directions['Directions']['Routes'][0]['Steps']:
#		f.write(step['descriptionHtml'])
#	f.write('</body></html>')

def getLocation():
#	storage = Storage('latitude.dat')
#	credentials = storage.get()
#	if credentials is None or credentials.invalid == True:
#		auth_discovery = build("latitude", "v1").auth_discovery()
#		flow = FlowThreeLegged(auth_discovery,
#			consumer_key = 'anonymous',
#			consumer_secret = 'AIzaSyAS8qvit6vX6ztCbHzYfnxKFoKTN-vZEY0',
#			user_agent = 'google-api-client-python-latitude/1.0',
#			scope = 'https://www.googleapis.com/auth/latitude',
#			xoauth_displayname = '18549 Location Query',
#			location = 'current',
#			granularity = 'best')
#		credentials = run(flow, storage)
#	http = httplib2.Http()
#	http = credentials.authorize(http)
#
#	p = build("latitude", "v1", http=http)
#	cl = p.currentLocation()
#	curLocation = cl.get().execute()
#	print curLocation
	curLocation = "Carnegie Mellon University, 5000 Forbes Avenue, Pittsburgh PA 15213"
	# hard coding address for simplicity and since geolocation is a solved problem
	return curLocation
	
def MapOrYT(string):
	#assumes string has format "<tag>value"
	tagStart = string.find('<')
	tagEnd = string.find('>')
	tag = string[tagStart+1:tagEnd]
	value = string[tagEnd+1:]
	if(tag == 'map'):
		#launch google maps with address
		GoogleMapAddress(value)
	elif(tag == 'media'):
		#launch youtube with search query
		YoutubeLink(value)
	else:
		print "Improperly Formatted String:" + string

if __name__ == '__main__':
	#will be changed to accept string from Jason's code when integrated
	if (len(sys.argv) > 1):
		content = sys.argv[1]
	else:
		content = "<media>cats"
	MapOrYT(content)
