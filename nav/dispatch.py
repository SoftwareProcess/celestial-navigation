import adjust
import predict
import correct
import locate

def dispatch(values=None):

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

    #Perform designated function
    if(values['op'] == 'adjust'):
        result = adjust.adjust(values)
        return result    
    elif(values['op'] == 'predict'):
        result = predict.predict(values)
        return result    
    elif(values['op'] == 'correct'):
        result = correct.correct(values)
        return result    
    elif(values['op'] == 'locate'):
        result = locate.locate(values)
        return result    
    else:
        values['error'] = 'op is not a legal operation'
        return values


