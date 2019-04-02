import unittest
import httplib
from urllib import urlencode
import json
import nav.correct as nav
import nav.dispatch as dispatch

class correctTest(unittest.TestCase):
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





# 100 predict
#    Analysis
#        inputs
#            observation -> string, mandatory, validated
#            height -> string, not mandatory, validated
#            temperature -> string, not mandatory, validated
#            pressure -> string, not mandatory, validated
#            horizon -> string, not mandatory, validated
#        outputs
#            altitude -> string, mandatory, validated
#            observation -> string, mandatory, validated
#            height -> string, not mandatory, validated
#            temperature -> string, not mandatory, validated
#            pressure -> string, not mandatory, validated
#            horizon -> string, not mandatory, validated
#    Happy path analysis
#        strategy: exercise code from simple to hard
#        1) return a constant
#        2) return a dictionary
#        3) return the correct dip
#        4) return the correct refraction
#        5) return the correct altitude
#        6) round altitude to nearest 0.1 arc-minute
#        7) check if adjust can return desired dictionary


#     def test100_010ShouldVerifyCallToCorrect(self):
#         expectedResult = 1.0
#         actualResult = nav.correct()
#         self.assertEquals(expectedResult, actualResult)

#     def test100_020ShouldReturnDictionary(self):
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','-53d38.4')
#         self.setParm('assumedLong','350d35.3') 
#         expectedResult = {'altitude':'13d42.3', 
#                           'assumedLat': '-53d38.4', 
#                           'assumedLong': '350d35.3',  
#                           'long': '95d41.6', 
#                           'op': 'correct',
#                           'lat': '16d32.3'}     
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(expectedResult, actualResult)
        
#     def test100_030ShouldCalculateLHA(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','-53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         expectedResult = "446d16.9"
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(expectedResult, actualResult)
        
    def test100_040ShouldCalculateIntermediateDistance(self): 
        self.setParm('op','correct')
        self.setParm('lat','16d32.3')
        self.setParm('long','95d41.6')
        self.setParm('altitude','13d42.3')
        self.setParm('assumedLat','53d38.4')
        self.setParm('assumedLong','350d35.3')
        expectedResult = 0.266093465
        actualResult = nav.correct(self.inputDictionary)
        self.assertAlmostEquals(expectedResult, actualResult, 3)    
