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

import json
import xmltodict

def printPrettyDict(d):
    print(json.dumps(d, sort_keys=True, indent=4, separators=(',', ': ')))


class ParseNxtbus:
	def __init__(self,responseDict):
		jsonData =  xmltodict.parse(responseDict)
		self._data = jsonData

	def stopMonitoring(self):
		serviceDelivery = self._data["Siri"]["ServiceDelivery"]
		arrivals = []
		if "StopMonitoringDelivery" in serviceDelivery:

			if "MonitoredStopVisit" in serviceDelivery["StopMonitoringDelivery"]:

			    monitoredBuses = serviceDelivery["StopMonitoringDelivery"]["MonitoredStopVisit"]

			    # Check if there is more than one bus arriving
			    if "MonitoredVehicleJourney" in monitoredBuses:
			    	busJourney = self._parseBusJourney(monitoredBuses)
			    	if busJourney:
			    		arrivals.append(busJourney)

			    else:
			    	for journey in monitoredBuses:
				    	busJourney = self._parseBusJourney(journey)
				    	if busJourney:
				    		arrivals.append(busJourney)
		return arrivals

	def _parseBusJourney(self,busJourneyDictionary):
		if "AimedDepartureTime" in busJourneyDictionary["MonitoredVehicleJourney"]["MonitoredCall"]: # Is departing
			bus = busJourneyDictionary["MonitoredVehicleJourney"]
			busJourney = {}

			busJourney["busRouteNumber"] = bus["ExternalLineRef"]
			busJourney["destinationName"] = bus["DestinationName"]

			if bus["Monitored"] == "true":
			    busJourney["departureTime"] = bus["MonitoredCall"]["ExpectedDepartureTime"]
			    busJourney["monitored"] = True
			else:
			    busJourney["departureTime"] = bus["MonitoredCall"]["AimedDepartureTime"]
			    busJourney["monitored"] = False
			return busJourney
		return None
