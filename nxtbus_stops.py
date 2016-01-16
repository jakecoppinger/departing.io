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
