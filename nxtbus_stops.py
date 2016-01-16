import csv

class NxtbusStops():
	def __init__(self,csvFilename):
		data = []
		for row in csv.DictReader(open(csvFilename)):
			data.append(row)
		self._allData = data

	def busStopIDDictionary(self):
		busStops = {}
		for row in self._allData:
			busStops[row["Stop"]] = row
		return busStops
		
	def addressDictionary(self):
		addresses = {}
		for row in self._allData:
			addresses[row["Description"]] = row
		return addresses

	def addressList(self):
		addresses = []
		for row in self._allData:
			addresses.append(row["Description"])
		return addresses
