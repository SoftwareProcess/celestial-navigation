import adjust
def dispatch(values=None):

    #Validate parm
    if(values == None):
        return {'error': 'parameter is missing'}
    if(not(isinstance(values,dict))):
        return {'error': 'parameter is not a dictionary'}
    if ('error' in values):
        values.pop('error')
        return values
    if (not('op' in values) or values['op'] == ''):
        values['error'] = 'no op  is specified'
        return values
    if (not(values['op'] == 'adjust')):
        values['error'] = 'op is not a legal operation'
        return values
    if (values.has_key('altitude')):
        values['error'] = 'altitude already exist'
        return values
    if (not(values.has_key('observation'))):
        values['error'] = 'observation is missing'
        return values
    if ('d' not in values['observation']):
        values['error'] = 'observation does not contain d'
        return values
    x, y = values['observation'].split('d')
    if (int(x) < 1 or int(x) >= 90 or float(y) < 0 or float(y) >= 60):
        values['error'] = 'observation is invalid'
        return values
    
    
    if (not(values.has_key('height'))):
        values['height'] = '0' 
    if (values['height'].isdigit()):
        values['error'] = 'height is not numeric'    
        return values 
    if (float(values['height']) < 0):
        values['error'] = 'height is invalid'
        return values
    
    if (not(values.has_key('temperature'))):
        values['temperature'] = '72'
#     if (not(values['temperature'].isint())):
#         values['error'] = 'temperature is not an integer'    
#         return values
    if (int(values['temperature']) > 120 or int(values['temperature']) < -20):
        values['error'] = 'temperature is out of bound'
        return values
    
#     if (not(values['pressure'].isint())):
#         values['error'] = 'pressure is not an integer'    
#         return values
    if (int(values['pressure']) > 1100 ):
        values['error'] = 'pressure is out of bound'
        return values
    
    

    #Perform designated function
    if(values['op'] == 'adjust'):
        result = adjust.adjust(values)
        return result    
    elif(values['op'] == 'predict'):
        return values    #This calculation is stubbed out
    elif(values['op'] == 'correct'):
        return values    #This calculation is stubbed out
    elif(values['op'] == 'locate'):
        return values    #This calculation is stubbed out
    else:
        values['error'] = 'op is not a legal operation'
        return values


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