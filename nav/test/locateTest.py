import unittest
import httplib
from urllib import urlencode
import json
import nav.locate as nav
import nav.dispatch as dispatch

class predictTest(unittest.TestCase):
    def setUp(self):
        self.inputDictionary = {}
        self.errorKey = "error"
        self.solutionKey = "probability"
        self.BX_PATH = '/nav?'
        self.BX_PORT = 5000
        self.BX_URL = 'localhost'
#         self.BX_PORT = 5000
#         self.BX_URL = 'www.ibmcloud.com'

    def tearDown(self):
        self.inputDictionary = {}

    def setParm(self, key, value):
        self.inputDictionary[key] = value
        
    def microservice(self):
        try:
            theParm = urlencode(self.inputDictionary)
            theConnection = httplib.HTTPConnection(self.BX_URL, self.BX_PORT)
            theConnection.request("GET", self.BX_PATH + theParm)
            theStringResponse = theConnection.getresponse().read()
            return theStringResponse
        except Exception as e:
            return "error encountered during transaction"
        
    def string2dict(self, httpResponse):
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = httpResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element],unicode)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result


    def test100_010ShouldVerifyCallToLocate(self):
        expectedResult = 1.0
        actualResult = nav.locate(expectedResult)
        self.assertEquals(expectedResult, actualResult)
        
        
    def test100_020ShouldReturnDictionary(self):
        self.setParm('op','locate')
        self.setParm('assumedLat','-53d38.4')
        self.setParm('assumedLong','350d35.3') 
        self.setParm('corrections','[[100,1d0.1]]')
        expectedResult = {'assumedLat': '-53d38.4', 
                          'assumedLong': '350d35.3', 
                          'corrections': '[[100,1d0.1]]',   
                          'op': 'locate'}     
        actualResult = nav.locate(self.inputDictionary)
        self.assertEquals(expectedResult, actualResult)
