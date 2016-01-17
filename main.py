# Departing.io, a web app to answer the question of "When will the next bus come?"
# Copyright (C) 2016 Jake Coppinger

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import json

from tornado.options import define, options

from handlers import *
from nxtbus_stops import NxtbusStops

define("host", default="localhost", help="app host (domain)", type=str)
define("production",default=0, help="1 if in production, 0 if local", type=int)

port = os.environ.get("PORT", 5000) # 5000 is Heroku's default port

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			# GUI Handlers
			(r'/', IndexHandler),
			(r'/debug', DebugHandler),
			# Python API Functions
			(r'/departures', StopDeparturesHandler),
            (r'/departures_post', DeparturesPostHandler),
			(r'/validstopid', ValidStopIDHandler),
			(r'/closeststop',ClosestStopHandler),
			 ]
		
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__),"static"),
			debug=True
			)

		self.apiKey = os.environ['NXTBUS_API_KEY']

		officialStopData = NxtbusStops("data/bus_stops.csv")
		humanizedStopData = NxtbusStops("data/humanized_bus_stops.csv")

		self.stopIDs = officialStopData.busStopIDDictionary()
		self.addressIDs = officialStopData.addressDictionary()

		self.humanAddressDictionary = humanizedStopData.addressDictionary()
		self.humanAddressList = humanizedStopData.addressList()

		if(options.production == 1):
			self.port = 80
		else:
			self.port = os.environ.get("PORT", 5000)
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())

	http_server.listen(port)
	print("Departing.io Copyright (C) 2016 Jake Coppinger")
	print("Server starting at http://" + options.host + ":" + str(port) + "/")
	tornado.ioloop.IOLoop.instance().start()