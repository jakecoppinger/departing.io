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


