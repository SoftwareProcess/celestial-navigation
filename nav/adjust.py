from math import sqrt, tan, pi

def adjust(values = None):
    def isint(arg):
        try:
            int(arg)
            return True
        except ValueError:
            return False        
    def isfloat(arg):
        try:
            float(arg)
            return True
        except ValueError:
            return False
    #Validate parameters
  
#     if (values.has_key('altitude')):
#         values['error'] = 'altitude already exist'
#         return values   
    if (not(values.has_key('observation'))):
        values['error'] = 'observation is missing'
        return values
    if ('d' not in values['observation']):
        values['error'] = 'observation does not contain d'
        return values
    x, y = values['observation'].split('d')
    x = x.lstrip('0')
    y = y.lstrip('0')
    if (int(x) < 1 or int(x) >= 90 or float(y) < 0 or float(y) >= 60):
        values['error'] = 'observation is invalid'
        return values  
    values['observation'] = x + 'd' + y
    if (not(values.has_key('height'))):
        height = 0 
    elif (not(isint(values['height'])) or not(isfloat(values['height']))):
        values['error'] = 'height is not numeric'    
        return values 
    elif (int(values['height']) < 0):
        values['error'] = 'height is invalid'
        return values     
    if (not(values.has_key('temperature'))):
        temperature = 72
    elif (not(isint(values['temperature']))):
        values['error'] = 'temperature is not an integer'    
        return values
    elif (int(values['temperature']) > 120 or int(values['temperature']) < -20):
        values['error'] = 'temperature is out of bound'
        return values  
    if (not(values.has_key('pressure'))):
        pressure = 1010
    elif (not(isint(values['pressure']))):
        values['error'] = 'pressure is not an integer'    
        return values
    elif (int(values['pressure']) > 1100 or int(values['pressure']) < 100):
        values['error'] = 'pressure is out of bound'
        return values  
    if (not(values.has_key('horizon'))):
        horizon = 'natural' 
    elif (not(values['horizon'] == 'natural') and not(values['horizon'] == 'artificial')):
        values['error'] = 'horizon is invalid'
        return values  
     
    d, m =  values['observation'].split('d')
    degrees = float(d) + float(m) / 60
    radians = float(degrees * pi / 180)
    if (values.has_key('height')):
        height = int(float(values['height']))
    if (values.has_key('temperature')):    
        temperature = int(values['temperature'])
    if (values.has_key('pressure')):
        pressure = int(values['pressure'])
    if (values.has_key('horizon') and values['horizon'] == 'artificial'):
        dip = 0 
    else:  
        dip = -0.97 * sqrt(height) / 60 
        
    refraction = (-0.00452 * pressure) / (273 + (temperature-32) * 5 / 9) / tan(radians)
    altitude = degrees + dip + refraction
    x = int(altitude)
    y = round(altitude % 1 * 60, 1)
    altitude = str(x) + 'd' + str(y) 
    values['altitude'] = altitude
    
    result = values
    return result