from nxtbus import Nxtbus
from stop_monitoring_request import StopMonitoringRequest
from parse_nxtbus import ParseNxtbus
from tornado.options import define, options

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import json
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.httpclient

def dictToJson(d):
    print(json.dumps(d, sort_keys=True, indent=4, separators=(',', ': ')))

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', host=options.host, port=self.application.port)
		print(self.application.port)

class DebugHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('canvas_debug.html')

class DeparturesPostHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('departures_post.html')

class StopDeparturesHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		busStopID = int(self.get_argument('stop_id'))
		previewTime = int(self.get_argument('preview_time'))
		
		requestJSON = StopMonitoringRequest(self.application.apiKey,busStopID,previewTime).request()
		nxtbusServer = Nxtbus(self.application.apiKey)
		requestXML = nxtbusServer.stopRequestXML(requestJSON)
		requestURL = nxtbusServer.stopRequestURL()
		headers = {"Content-Type":"application/xml" }

		client = tornado.httpclient.AsyncHTTPClient()
		client.fetch(requestURL, method="POST",headers=headers,body=requestXML,callback=self.on_response)

	def on_response(self,response):
		arrivals = ParseNxtbus(response.body).stopMonitoring()
		self.write(tornado.escape.json_encode(arrivals))
  		self.finish()

class ValidStopIDHandler(tornado.web.RequestHandler):
	def post(self):
		busStopID = self.get_argument('stop_id')
		if busStopID in self.application.stopIDs:
			output = True
			print(self.application.stopIDs[busStopID])
		else:
			output = False
			print("Stop " + busStopID + " does not exist.")
		self.write(tornado.escape.json_encode(output))

class ClosestStopHandler(tornado.web.RequestHandler):
	def findEligibleStops(self,searchTerm):
		possibleStops = []
		# Number matching
		if len(searchTerm) <= 4 and searchTerm.isdigit():
			stopID = "0" * (4 - len(searchTerm)) + str(searchTerm)

			if stopID in self.application.stopIDs:
				shortAddress = self.application.stopIDs[stopID]["Description"]
				possibleStops.append({"value":shortAddress,"id": stopID})
				print("number exists")
			else:
				print("Number doesnt exist")
		else:
			# Fuzzy matching
			fuzzySearchResults = process.extract(searchTerm, self.application.humanAddressList,limit=7)
			for humanAddress in fuzzySearchResults:
				stopObject = self.application.humanAddressDictionary[humanAddress[0]] # Takes the first element (second is match value)
				stopID = stopObject["Stop"]
				shortAddress = self.application.stopIDs[stopID]["Description"]
				possibleStops.append({"value":shortAddress,"id": stopID})

		if len(possibleStops) == 0:
			possibleStops.append({"value":"No stops found","id": "0000"})

		return possibleStops

	def post(self):
		searchTerm = self.get_argument('search_term').strip()
		stops = self.findEligibleStops(searchTerm)
		self.write(tornado.escape.json_encode(stops))




	