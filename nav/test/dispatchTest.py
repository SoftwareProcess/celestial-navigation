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

    def test100_010ShouldReturnCorrectDict(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('height','33')
        self.setParm('temperature','72')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result['altitude']=='13d42.3', True)
    
    def test100_020ShouldReturnCorrectHeightWhenMissing(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('temperature','72')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        result = nav.dispatch(self.inputDictionary) 
        self.assertEquals(result['height'], '0')
     
    def test100_030ShouldReturnCorrectTemperatureWhenMissing(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('height','33')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['temperature'], '72')
     
    def test100_040ShouldReturnCorrectPressureWhenMissing(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('height','33')
        self.setParm('temperature','72')
        self.setParm('horizon','natural')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['pressure'], '1010')
     
    def test100_050ShouldReturnCorrectHorizonWhenMissing(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('height','33')
        self.setParm('temperature','72')
        self.setParm('pressure','1010')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['horizon'], 'natural')
#         
#  
#     # Sad path
    def test100_910_ShouldReturnValuesWithErrorKeyWhenNoOpSpecified(self):
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertTrue(resultDictionary.has_key("error"), True)
                 
    def test100_911ShouldReturnValuesWithErrorWhenContainErrorKey(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('error','unknown')
        result = nav.dispatch(self.inputDictionary)
        self.assertFalse(result.has_key("error"))    
         
    def test100_912ShouldReturnValuesWithErrorWhenParameterIsNotALegalOperation(self):
        self.setParm('op','unknown')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
          
    def test100_913ShouldReturnValuesWithErrorWhenOpIsBlank(self):
        self.setParm('op','')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                 
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
#         self.setParm('observation','45d12')        
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
# #########################################################################################      
#    
#     def test100_950ShouldReturnValuesWithErrorWhenHeightNotNumerical(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','33d12.5')
#         self.setParm('height','a')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#                
#     def test100_951ShouldReturnValuesWithErrorWhenHeightOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','33d12.5')
#         self.setParm('height','-4')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#              
#     def test100_960ShouldReturnValuesWithErrorWhenTemperatureNotInteger(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','33d12.5')
#         self.setParm('height','0')
#         self.setParm('temperature','140')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#          
#     def test100_961ShouldReturnValuesWithErrorWhenTemperatureOutOfUpperBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','33d12.5')
#         self.setParm('temperature','123')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#                 
#     def test100_962ShouldReturnValuesWithErrorWhenTemperatureOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','33d12.5')
#         self.setParm('temperature','-30')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#                
#     def test100_970ShouldReturnValuesWithErrorWhenPressureNotInteger(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','33d12.5')
#         self.setParm('pressure','a')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
#               
#     def test100_971ShouldReturnValuesWithErrorWhenPressureOutOfUpperBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation', '33d12.5')
#         self.setParm('pressure','1111')
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True) 
#    
#     def test100_982ShouldReturnValuesWithErrorWhenPressureOutOfLowerBound(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('pressure','99')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True) 
#        
#     def test100_990ShouldReturnValuesWithErrorWhenHorizonInvalid(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','45d12')
#         self.setParm('horizon','invalid')        
#         result = self.microservice()
#         resultDictionary = self.string2dict(result)
#         self.assertTrue(resultDictionary.has_key("error"), True)
# #         
# #     
# #           
# #      
# #      
