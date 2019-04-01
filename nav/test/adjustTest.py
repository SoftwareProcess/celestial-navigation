import unittest
import nav.adjust as nav
import nav.dispatch as dispatch
from urllib import urlencode
import httplib
import json


class adjustTest(unittest.TestCase):
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





# 500 adjust
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





#     def test500_010ShouldVerifyCallToAdjust(self):
#         expectedResult = 1.0
#         actualResult = nav.adjust()
#         self.assertEquals(expectedResult, actualResult)
        
#     def test500_020ShouldReturnDictionary(self):
#         values = self.setParm('op','adjust')
#         expectedResult = values
#         actualResult = nav.adjust(values)
#         self.assertEquals(expectedResult, actualResult)

#     def test500_030CalculateDip(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('temperature','72')
#         self.setParm('pressure','1010')
#         values = self.string2dict(self.microservice())
#         expectedResult = -0.092870429
#         actualResult = nav.adjust(values)
#         self.assertAlmostEquals(expectedResult, actualResult)       
    
#     def test500_040CalculateRefraction(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('temperature','72')
#         self.setParm('pressure','1010') 
#         values = self.string2dict(self.microservice())
#         expectedResult = -0.062673129
#         actualResult = nav.adjust(values)
#         self.assertAlmostEquals(expectedResult, actualResult, 4)
    
#     def test500_050Calculatealtitude(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('temperature','72')
#         self.setParm('pressure','1010') 
#         values = self.string2dict(self.microservice())
#         expectedResult = 13.70445644
#         actualResult = nav.adjust(values)
#         self.assertAlmostEquals(expectedResult, actualResult, 4)  
        
#     def test500_060Roundaltitude(self):
#         self.setParm('op','adjust')
#         self.setParm('observation','13d51.6')
#         self.setParm('height','33')
#         self.setParm('temperature','72')
#         self.setParm('pressure','1010') 
#         values = self.string2dict(self.microservice())
#         expectedResult = '13d42.3'
#         actualResult = nav.adjust(values)
#         self.assertEquals(expectedResult, actualResult)  
    
    def test500_010GeneralTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d15.2')
        self.setParm('height','6')
        self.setParm('temperature','71')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'45d11.9', 
                          'observation': '45d15.2', 
                          'height': '6', 
                          'pressure': '1010', 
                          'horizon': 'natural', 
                          'op': 'adjust',
                          'temperature': '71'}      
        self.assertEquals(expectedResult, actualResult)
        
    def test500_020GeneralTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','42d0.0')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'41d59.0', 
                          'observation': '42d0.0', 
                          'op': 'adjust'}      
        self.assertEquals(expectedResult, actualResult)
    
    def test500_030GeneralTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','42d0.0')
        self.setParm('extraKey','ignore')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'41d59.0', 
                          'observation': '42d0.0', 
                          'op': 'adjust',
                          'extraKey': 'ignore'}      
        self.assertEquals(expectedResult, actualResult)
     
    def test500_040ReplaceAltitudeTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','42d0.0')
        self.setParm('altitude','00d0.0')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'41d59.0', 
                          'observation': '42d0.0', 
                          'op': 'adjust'}      
        self.assertEquals(expectedResult, actualResult)    
    
    
    def test500_050LeadingZeroInXTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','045d15.2')
        self.setParm('height','6')
        self.setParm('temperature','71')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'45d11.9', 
                          'observation': '45d15.2', 
                          'height': '6', 
                          'pressure': '1010', 
                          'horizon': 'natural', 
                          'op': 'adjust',
                          'temperature': '71'}      
        self.assertEquals(expectedResult, actualResult)    
        
    def test500_060LeadingZeroInYTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','45d0015.2')
        self.setParm('height','6')
        self.setParm('temperature','71')
        self.setParm('pressure','1010')
        self.setParm('horizon','natural')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'45d11.9', 
                          'observation': '45d15.2', 
                          'height': '6', 
                          'pressure': '1010', 
                          'horizon': 'natural', 
                          'op': 'adjust',
                          'temperature': '71'}      
        self.assertEquals(expectedResult, actualResult)
        
    def test500_061AnotherLeadingZeroInYTest(self):
        self.setParm('op','adjust')
        self.setParm('observation','42d0000.0')
        self.setParm('altitude','00d0.0')
        actualResult = nav.adjust(self.inputDictionary)   
        expectedResult = {'altitude':'41d59.0', 
                          'observation': '42d0.0', 
                          'op': 'adjust'}      
        self.assertEquals(expectedResult, actualResult)  
        

    
    
      
    #sad path tests    
    def test900_040NoOpSpecifiedTest(self):
        self.setParm('op','')
        self.setParm('observation','42d0.0')
        actualResult = dispatch.dispatch(self.inputDictionary)         
        self.assertEquals(actualResult['error'], 'no op  is specified')
    
    def test900_050NoOpSpecifiedTest(self):
        self.setParm('op','')
        self.setParm('observation','42d0.0')
        actualResult = dispatch.dispatch(self.inputDictionary)         
        self.assertEquals(actualResult['error'], 'no op  is specified')
        
    def test900_060ShouldHaveAtleastOneDigitRightDecimal(self):
        self.setParm('op','adjust')
        self.setParm('observation','42d0')
        actualResult = dispatch.dispatch(self.inputDictionary)         
        self.assertEquals(actualResult['error'], 'must have at least one digit to the right of the decimal point')    
        
    
        
    
    
