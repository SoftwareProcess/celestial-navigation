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
    #                     return correct altitude
    #                     return correct height if missing
    #                     return correct temperature if missing
    #                     return correct pressure if missing
    #                     return correct horizon if missing

    #                     
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
    #     
    #                         return error when op is blank
    #                     return error when dictionary is invalid
    #                     return error when no dictionary input
    #                     return error when altitude present in input
    #                     return error when observation missing
    #                     return error when observation x out of upper bound
    #                     return error when observation x out of lower bound
    #                     return error when observation y out of upper bound
    #                     return error when observation y out of lower bound
    #                     return error when observation d missing
    #                     return error when height is not numerical
    #                     return error when height out of lower bound
    #                     return error when temperature is not integer
    #                     return error when temperature out of upper bound
    #                     return error when temperature out of lower bound
    #                     return error when pressure is not integer
    #                     return error when pressure out of upper bound
    #                     return error when pressure out of lower bound
    #                     return error when horizon is invalid 
    #                     
    # Happy path

    def test100_010ShouldReturnCorrectAltitude(self):
        self.setParm('op','adjust')
        self.setParm('observation','13d51.6')
        self.setParm('height','33')
        self.setParm('temperature','72')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result['altitude']=='13d42.3', True)
    
#     def test100_020ShouldReturnCorrectHeightWhenMissing(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('temperature','72')
#         self.setParm('pressure','1010')
#         self.setParm('horizon','natural')
#         result = nav.dispatch(self.inputDictionary) 
#         self.assertEquals(result['height'], '0')
#      
#     def test100_030ShouldReturnCorrectTemperatureWhenMissing(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('pressure','1010')
#         self.setParm('horizon','natural')
#         result = nav.dispatch(self.inputDictionary)
#         self.assertEquals(result['temperature'], '72')
#      
#     def test100_040ShouldReturnCorrectPressureWhenMissing(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('temperature','72')
#         self.setParm('horizon','natural')
#         result = nav.dispatch(self.inputDictionary)
#         self.assertEquals(result['pressure'], '1010')
#      
#     def test100_050ShouldReturnCorrectHorizonWhenMissing(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('temperature','72')
#         self.setParm('pressure','1010')
#         result = nav.dispatch(self.inputDictionary)
#         self.assertEquals(result['horizon'], 'natural')
#         
#  
#     # Sad path
    def test100_910_ShouldReturnValuesWithErrorKeyWhenNoOpSpecified(self):
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                 
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
                 
    def test100_920ShouldReturnValuesWithErrorWhenNotDictionary(self):            
        result = nav.dispatch(42)
        self.assertTrue(result.has_key("error"), True)
                
    def test100_921ShouldReturnValuesWithErrorWhenDictionaryMissing(self):         
        result = nav.dispatch()
        self.assertTrue(result.has_key("error"), True)
             
    def test100_930ShouldReturnValuesWithErrorWhenAltitudePresent(self):
        self.setParm('op','adjust')
        self.setParm('altitude','a')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
             
    def test100_940ShouldReturnValuesWithErrorWhenObservationMissing(self):
        self.setParm('op','adjust')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
             
    def test100_941ShouldReturnValuesWithErrorWhenObservationXOutOfUpperBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','90d15.2')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
         
    def test100_942ShouldReturnValuesWithErrorWhenObservationXOutOfLowerBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','0d15.2')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
              
    def test100_943ShouldReturnValuesWithErrorWhenObservationYOutOfUpperBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d70')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                
    def test100_944ShouldReturnValuesWithErrorWhenObservationYOutOfLowerBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d-1')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                  
    def test100_945ShouldReturnValuesWithErrorWhenObservationDMissing(self):
        self.setParm('op','adjust')
        self.setParm('observation','31')           
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
     
    
    def test100_950ShouldReturnValuesWithErrorWhenHeightNotNumerical(self):
        self.setParm('op','adjust')
        self.setParm('observation','33d12.5')
        self.setParm('height','a')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                
    def test100_951ShouldReturnValuesWithErrorWhenHeightOutOfLowerBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','33d12.5')
        self.setParm('height','-4')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
              
    def test100_960ShouldReturnValuesWithErrorWhenTemperatureNotInteger(self):
        self.setParm('op','adjust')
        self.setParm('observation','33d12.5')
        self.setParm('height','0')
        self.setParm('temperature','140')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
          
    def test100_961ShouldReturnValuesWithErrorWhenTemperatureOutOfUpperBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','33d12.5')
        self.setParm('temperature','123')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                 
    def test100_962ShouldReturnValuesWithErrorWhenTemperatureOutOfLowerBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','33d12.5')
        self.setParm('temperature','-30')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
                
    def test100_970ShouldReturnValuesWithErrorWhenPressureNotInteger(self):
        self.setParm('op','adjust')
        self.setParm('observation','33d12.5')
        self.setParm('pressure','a')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)
               
    def test100_971ShouldReturnValuesWithErrorWhenPressureOutOfUpperBound(self):
        self.setParm('op','adjust')
        self.setParm('observation', '33d12.5')
        self.setParm('pressure','1111')
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True) 
    
    def test100_982ShouldReturnValuesWithErrorWhenPressureOutOfLowerBound(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d12')
        self.setParm('pressure','99')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True) 
        
    def test100_990ShouldReturnValuesWithErrorWhenHorizonInvalid(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d12')
        self.setParm('horizon','invalid')        
        result = nav.dispatch(self.inputDictionary)
        self.assertTrue(result.has_key("error"), True)

# acceptance test for predict
     
    def test200_010ShouldReturnCorrectResult(self):
        self.setParm('op','predict')
        self.setParm('body','Aldebaran')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['op'], 'predict')
        self.assertEquals(result['body'], 'Aldebaran')
        self.assertEquals(result['date'], '2016-01-17')
        self.assertEquals(result['time'], '03:15:42')
        self.assertEquals(result['long'], '95d41.6')       
        self.assertEquals(result['lat'], '16d32.3') 
    
    def test200_015ShouldReturnCorrectResult(self):
        self.setParm('op','predict')
        self.setParm('body','Betelgeuse')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['op'], 'predict')
        self.assertEquals(result['body'], 'Betelgeuse')
        self.assertEquals(result['date'], '2016-01-17')
        self.assertEquals(result['time'], '03:15:42')
        self.assertEquals(result['long'], '75d53.6')       
        self.assertEquals(result['lat'], '7d24.3') 
        
    def test800_010MissingBody(self):
        self.setParm('op','predict')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['error'], 'body is missing')
        
    def test800_020StarNotInCatalog(self):
        self.setParm('op','predict')
        self.setParm('body','unknown')
        self.setParm('date','2016-01-17')
        self.setParm('time','03:15:42')
        result = nav.dispatch(self.inputDictionary)
        self.assertEquals(result['op'], 'predict')
        self.assertEquals(result['body'], 'unknown')
        self.assertEquals(result['date'], '2016-01-17')
        self.assertEquals(result['time'], '03:15:42')
        self.assertEquals(result['error'], 'star not in catalog')       
       
# acceptance test for predict
    def test300_010ShouldReturnCorrectResult(self):
        self.setParm('op','correct')
        self.setParm('lat','89d20.1')
        self.setParm('long','154d5.4')
        self.setParm('altitude','37d15.6')
        self.setParm('assumedLat','33d59.7')
        self.setParm('assumedLong','74d35.3')
        actualResult = nav.dispatch(self.inputDictionary)
        self.assertEquals(actualResult['correctedDistance'], '222')
        self.assertEquals(actualResult['correctedAzimuth'], '0d36.0')  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
