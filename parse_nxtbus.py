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
