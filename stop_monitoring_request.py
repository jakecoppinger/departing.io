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

import datetime
import json
import dicttoxml
import xmltodict

class StopMonitoringRequest:
  siriVersionTag = '<Siri xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" version="2.0" xmlns="http://www.siri.org.uk/siri">'

  def __init__(self,apiKey,busStopID,previewInterval=30):

    requestTimestamp = self._generateTimestamp()
    self._request =  {"ServiceRequest": {"RequestTimestamp": requestTimestamp,
      "RequestorRef": apiKey,"StopMonitoringRequest": {
        "-version": "2.0",
        "RequestTimestamp": requestTimestamp
       # "PreviewInterval": "PT1H"
       # "MonitoringRef": busStopID
       # "MaximumStopVisits": "4"
       # "MaximumTextLength": "160"
      }}}

    self.busStop(busStopID)
    self.previewInterval(previewInterval)

  def _generateTimestamp(self):
    return datetime.datetime.now().isoformat()


  def previewInterval(self,minutes):
    intervalString = "PT" + str(minutes) + "M"
    self._request["ServiceRequest"]["StopMonitoringRequest"]["PreviewInterval"] = intervalString

  def busStop(self,busStopID):
    self._request["ServiceRequest"]["StopMonitoringRequest"]["MonitoringRef"] = busStopID

  def maximumStopVisits(self,visits):
    self._request["ServiceRequest"]["StopMonitoringRequest"]["MaximumStopVisits"] = visits
  
  def request(self):
    return self._request

  def requestJSON(self):
    return json.dumps(self._request, sort_keys=True, indent=4, separators=(',', ': '))




