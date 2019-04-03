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
        
#     def test100_040ShouldCalculateIntermediateDistance(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         expectedResult = 0.266093465
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertAlmostEquals(expectedResult, actualResult, 3)    

#     def test100_050ShouldCalculatecorrectedAltitude(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         expectedResult = 0.269338106
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertAlmostEquals(expectedResult, actualResult, 3)

#     def test100_060ShouldConvertCorrectedAltitude(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         expectedResult = "15d25.9"
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(expectedResult, actualResult)


#     def test100_060ShouldCalculateCorrectedDistance(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         expectedResult = -104
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(expectedResult, actualResult)
        
#     def test100_070ShouldCalculateCorrectedAzimuth(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         expectedResult = "82d55.6"
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(expectedResult, actualResult)

#     def test100_080ShouldReturnDesiredOutput(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','16d32.3')
#         self.setParm('long','95d41.6')
#         self.setParm('altitude','13d42.3')
#         self.setParm('assumedLat','53d38.4')
#         self.setParm('assumedLong','350d35.3')
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(actualResult['correctedDistance'], '104')
#         self.assertEquals(actualResult['correctedAzimuth'], '262d55.6')

#     def test100_081ShouldReturnDesiredOutput(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','89d20.1')
#         self.setParm('long','154d5.4')
#         self.setParm('altitude','37d15.6')
#         self.setParm('assumedLat','33d59.7')
#         self.setParm('assumedLong','74d35.3')
#         actualResult = nav.correct(self.inputDictionary)
#         self.assertEquals(actualResult['correctedDistance'], '222')
#         self.assertEquals(actualResult['correctedAzimuth'], '0d36.0')

#     def test100_090ShouldReturnDesiredOutputThroughDispatch(self): 
#         self.setParm('op','correct')
#         self.setParm('lat','89d20.1')
#         self.setParm('long','154d5.4')
#         self.setParm('altitude','37d15.6')
#         self.setParm('assumedLat','33d59.7')
#         self.setParm('assumedLong','74d35.3')
#         actualResult = dispatch.dispatch(self.inputDictionary)
#         self.assertEquals(actualResult['correctedDistance'], '222')
#         self.assertEquals(actualResult['correctedAzimuth'], '0d36.0')
# 
# 
# #sad path tests
#     def test900_010MissingLat(self):       
#         self.setParm('op','correct')
#         actualResult = dispatch.dispatch(self.inputDictionary)
#         self.assertEquals(actualResult['error'], 'mandatory information is missing')

#     def test900_011LatIsNotValid(self):       
#         self.setParm('op','correct')
#         self.setParm('lat','8920.1')
#         actualResult = dispatch.dispatch(self.inputDictionary)
#         self.assertEquals(actualResult['error'], 'lat is not valid')

    def test900_012LatOutOfUpperBound(self):       
        self.setParm('op','correct')
        self.setParm('lat','90d20.1')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'lat is not valid')

    def test900_013LatOutOfLowerBound(self):       
        self.setParm('op','correct')
        self.setParm('lat','-90d0.0')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'lat is not valid')

    def test900_014MinutesNotInCorrectForm(self):       
        self.setParm('op','correct')
        self.setParm('lat','89d20')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'lat is not valid')



