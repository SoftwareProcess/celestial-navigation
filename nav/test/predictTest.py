import unittest
import httplib
from urllib import urlencode
import json
import nav.predict as nav
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





#     def test100_010ShouldVerifyCallToPredict(self):
#         expectedResult = 1.0
#         actualResult = nav.predict()
#         self.assertEquals(expectedResult, actualResult)
        
#     def test100_020ShouldReturnDictionary(self):
#         values = self.setParm('op','predict')
#         expectedResult = values
#         actualResult = nav.predict(values)
#         self.assertEquals(expectedResult, actualResult)
        
#     def test100_030ShouldReadStarDataAndOutPutNumberOfColumns(self):
#         expectedResult = 5
#         actualResult = nav.predict()
#         self.assertEquals(expectedResult, actualResult)
        
#     def test100_040SearchAStarFromStarData(self):
#         self.setParm('body','Hadar')
#         expectedResult = 'found'
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertEquals(actualResult, expectedResult)
        
#     def test100_050OutputDataForAStar(self):
#         self.setParm('body','Hadar')
#         expectedResult = '148d45.5-60d26.60.6'
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertEquals(actualResult, expectedResult)
        
#     def test100_060ShouldCalculateCumulativeProgression(self):
#         self.setParm('body','Aldebaran')
#         self.setParm('date','2016-01-17')
#         self.setParm('time','03:15:42')
#         expectedResult = -214.75
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertAlmostEquals(actualResult, expectedResult, 5)
        
#     def test100_070ShouldCalculateLeapProgression(self):
#         self.setParm('body','Aldebaran')
#         self.setParm('date','2016-01-17')
#         self.setParm('time','03:15:42')
#         expectedResult = 176.925
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertAlmostEquals(actualResult, expectedResult, 5)
     
#     def test100_080ShouldCalculateSeconds(self):
#         self.setParm('body','Aldebaran')
#         self.setParm('date','2016-01-17')
#         self.setParm('time','03:15:42')
#         expectedResult = 1394142
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertAlmostEquals(actualResult, expectedResult, 3) 
           
#     def test100_080ShouldCalculateTotalGHAAries(self):
#         self.setParm('body','Aldebaran')
#         self.setParm('date','2016-01-17')
#         self.setParm('time','03:15:42')
#         expectedResult = 9894.5
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertAlmostEquals(actualResult, expectedResult, 2) 
        
#     def test100_090ShouldCalculateTotalGHAStar(self):
#         self.setParm('body','Aldebaran')
#         self.setParm('date','2016-01-17')
#         self.setParm('time','03:15:42')
#         expectedResult = 5741.6
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertAlmostEquals(actualResult, expectedResult, 2) 

    def test100_090ShouldReturnCorrectLongAndLat(self):
        self.setParm('body','Aldebaran')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42')
        actualResult = nav.predict(self.inputDictionary)
        self.assertEquals(actualResult['long'], '95d41.6')
        self.assertEquals(actualResult['lat'], '16d32.3')
#         
    def test100_095ShouldReturnCorrectLongAndLat(self):
        self.setParm('body','Betelgeuse')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42')
        actualResult = nav.predict(self.inputDictionary)
        self.assertEquals(actualResult['long'], '75d53.6')
        self.assertEquals(actualResult['lat'], '7d24.3') 
        
    def test100_100BodyIsCaseIndependent(self):
        self.setParm('body','betelgeuse')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42')
        actualResult = nav.predict(self.inputDictionary)
        self.assertEquals(actualResult['long'], '75d53.6')
        self.assertEquals(actualResult['lat'], '7d24.3') 

#     def test200_010DefaultDateIfMissing(self):
#         self.setParm('body','Betelgeuse')
#         self.setParm('time','03:15:42')
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertEquals(actualResult, '2001-01-01')
#  
#     def test200_020DefaultTimeIfMissing(self):
#         self.setParm('body','Betelgeuse')
#         actualResult = nav.predict(self.inputDictionary)
#         self.assertEquals(actualResult, '00:00:00')
        
#sad path test        
    def test900_010MissingBody(self):       
        self.setParm('op','predict')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'body is missing') 
        
    def test900_020StarNotInData(self):       
        self.setParm('op','predict')
        self.setParm('body','unknown')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'star not in catalog')
        
    def test900_030InvalidDate(self):       
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')
        self.setParm('date','2200-01-17')
        self.setParm('time','03:15:42')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'invalid date')

    def test900_035InvalidDate(self):       
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:99')
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'invalid date')
        
    def test900_040DateAndTimeMustHaveTwoDigits(self):
        self.setParm('op','predict')       
        self.setParm('body','Betelgeuse')
        self.setParm('date','2016-01-17')
        self.setParm('time','3:15:42')        
        actualResult = dispatch.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['error'], 'date and time must have two digits')

