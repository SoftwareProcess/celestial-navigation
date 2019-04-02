from cmath import sin, cos


def correct(values = None):
    #helper function        
    def convertStrToMinutes(arg):
        x, y = arg.split('d')
        minutes = int(x) * 60 + float(y)
        return minutes  
    def convertMinutesToStr(arg):
        degree = int(arg / 60)
        minutes = round(arg % 60, 1)
        string = str(degree) + 'd' + str(minutes)
        return string
    def convertStrToDegrees(arg):
        x, y = arg.split('d')
        degrees = int(x) + float(y)/60
        return degrees
    
    
    LHA = convertStrToDegrees(values['long']) + convertStrToDegrees(values['assumedLong'])
    intermediateDistance = (sin(convertStrToDegrees(values['lat'])) 
        * sin(convertStrToDegrees(values['assumedLat']))) + (cos(convertStrToDegrees(values['lat'])) 
        * cos(convertStrToDegrees(values['assumedLat'])) * cos(LHA))
    
    return intermediateDistance 