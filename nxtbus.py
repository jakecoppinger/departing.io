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

import dicttoxml
import xmltodict

class Nxtbus:
    def __init__(self,apiKey):
        self.apiKey = apiKey

    def _createSiriRequest(self,dict):
        siriVersionTag = '<Siri xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" version="2.0" xmlns="http://www.siri.org.uk/siri">'
        rawXML = dicttoxml.dicttoxml(dict, attr_type=False,custom_root='Siri')
        return rawXML.replace("<Siri>",siriVersionTag)

    def _createRequestURL(self,serviceType):
        url = 'http://siri.nxtbus.act.gov.au:11000/%s/%s/service.xml' % (self.apiKey,serviceType)
        return url

    def stopMonitoringRequest(self,requestData):
        responseXML = self._nxtbusRequest('sm',requestData)
        return xmltodict.parse(responseXML)

    def stopRequestXML(self,requestJSON):
        return self._createSiriRequest(requestJSON)

    def stopRequestURL(self):
        return self._createRequestURL('sm')


