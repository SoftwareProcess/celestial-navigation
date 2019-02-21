import unittest
import httplib
from urllib import urlencode
import json

import nav.dispatch as nav

class DispatchTest(unittest.TestCase):
    
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


    # -----------------------------------------------------------------------
    # ---- Acceptance Tests
    # 100 dispatch operation
    #   Happy path analysis:
    #        values:      mandatory
    #                     dictionary
    #                     Operations:   {'op':'adjust'}
    #                                   {'op':'predict'}
    #                                   {'op':'correct'}
    #                                   {'op':'locate'}
    #   Sad path analysis:
    #        values:
    #                     no op specified             values={}
    #                        -- return {'error':'no op  is specified'}
    #                     contain 'error' as a key      values={5d04.9', 'height': '6.0', 'pressure': '1010',
    #                                                           'horizon': 'artificial', 'temperature': '72'
    #                                                           'error':'no op is specified'}'
    #                        -- return values without error as a key and without its values
    #                     not-dictionary                values=42
    #                        -- return {'error':'parameter is not a dictionary'}
    #                     not legal operation           values={'op': 'unknown'}
    #                        -- return {'error':'op is not a legal operation'}
    #                     missing dictionary            dispatch()
    #                        -- return {'error':'dictionary is missing'}
    # Happy path

#     def test100_010ShouldReturnUnchangedValuesWithOperationAdjust(self):
#         self.setParm('op','adjust')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertDictEqual(self.inputDictionary, resultDictionary)

#     def test100_020ShouldReturnUnchangedValuesWithOperationPredict(self):
#         self.setParm('op','predict')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertDictEqual(self.inputDictionary, resultDictionary)
#  
#     def test100_030ShouldReturnUnchangedValuesWithOperationCorrect(self):
#         self.setParm('op','correct')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertDictEqual(self.inputDictionary, resultDictionary)
#         
#     def test100_040ShouldReturnUnchangedValuesWithOperationLocate(self):
#         self.setParm('op','locate')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertDictEqual(self.inputDictionary, resultDictionary)


 
    # Sad path
#     def test100_910_ShouldReturnValuesWithErrorKeyWhenNoOpSpecified(self):
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#          
#     def test100_911ShouldReturnValuesWithErrorWhenContainErrorKey(self):
#         values = {'observation': '5d5', 'op': 'adjust', 'error': 'invalid', 'height': '30', 'temperature': '72', 'pressure': '1000'}         
#         result = nav.dispatch(values)
#         self.assertFalse(result.has_key("error"), True)    
#  
#     def test100_912ShouldReturnValuesWithErrorWhenParameterIsNotALegalOperation(self):
#         self.setParm('op','unknown')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#   
#     def test100_913ShouldReturnValuesWithErrorWhenOpIsBlank(self):
#         self.setParm('op','')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#          
#     def test100_920ShouldReturnValuesWithErrorWhenNotDictionary(self):  
#         values = 42         
#         result = nav.dispatch(values)
#         self.assertTrue(result.has_key("error"), True)
#          
#     def test100_921ShouldReturnValuesWithErrorWhenDictionaryMissing(self):         
#         result = nav.dispatch()
#         self.assertTrue(result.has_key("error"), True)
#      
#     def test100_930ShouldReturnValuesWithErrorWhenAltitudePresent(self):
#         self.setParm('op','adjust')
#         self.setParm('altitude','a')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#      
#     def test100_940ShouldReturnValuesWithErrorWhenObservationMissing(self):
#         self.setParm('op','adjust')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#      
#     def test100_941ShouldReturnValuesWithErrorWhenObservationXOutOfUpperBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','90d15.2')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#  
#     def test100_942ShouldReturnValuesWithErrorWhenObservationXOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','0d15.2')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#          
#     def test100_943ShouldReturnValuesWithErrorWhenObservationYOutOfUpperBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d60')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#          
#     def test100_944ShouldReturnValuesWithErrorWhenObservationYOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d-1')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#           
#     def test100_945ShouldReturnValuesWithErrorWhenObservationDMissing(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','31')           
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#   
#     def test100_950ShouldReturnValuesWithErrorWhenHeightNotNumerical(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('height','a')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#           
#     def test100_951ShouldReturnValuesWithErrorWhenHeightOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('height','-1')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#       
#     def test100_960ShouldReturnValuesWithErrorWhenTemperatureNotInteger(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('temperature','a')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
# 
#     def test100_961ShouldReturnValuesWithErrorWhenTemperatureOutOfUpperBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('temperature','123')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#         
#     def test100_962ShouldReturnValuesWithErrorWhenTemperatureOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('temperature','-12')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
        
    def test100_980ShouldReturnValuesWithErrorWhenPressureNotInteger(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d12')
        self.setParm('pressure','a')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertTrue(resultDictionary.has_key("error"), True)
    
