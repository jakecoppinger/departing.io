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




