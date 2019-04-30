from math import cos, radians, sin, sqrt


def locate(values = None):
    
    
    def convertStrToDegrees(arg):
        x, y = arg.split('d')
        if (int(x) >= 0):
            degrees = int(x) + float(y)/60
        else:
            degrees = int(x) - float(y)/60
        return degrees
    
    def convertStrToMinutes(arg):
        x, y = arg.split('d')
        if (int(x) >= 0):
            minutes = int(x) * 60 + float(y)
        else:
            minutes = int(x) * 60 - float(y)
        return minutes

    def convertMinutesToStr(arg):
        if (arg >= 0):
            degree = int(arg / 60)
            minutes = round(arg % 60, 1)
        else:
            degree = int(arg / 60)
            minutes = -(round(arg % -60, 1))   
        string = str(degree) + 'd' + str(minutes)           
        return string  
    
    def myRound(arg):
        temp = abs(arg)
        decimal = temp - int(temp)
        if (decimal < 0.5):
            temp = int(temp)
        else:
            temp = int(temp) + 1
        if (arg < 0):
            temp = -temp
        return temp  
 
    correctionString = values['corrections']
    correctionString = correctionString[1:-1]
    tempList = []
    for i in range(len(correctionString)):
        temp = ''
        if (correctionString[i] == '['):
            while (correctionString[i+1] != ']'):
                temp += correctionString[i+1]
                i += 1
            tempList.append(temp)
    numOfCorrections = len(tempList)

    tempSum = 0
    for i in range(numOfCorrections):
        corDis, corAzm = tempList[i].split(',') 
        tempSum = tempSum + float(corDis) * cos(radians(convertStrToDegrees(corAzm))) 
    nsCorrection = tempSum / numOfCorrections
    
    tempSum = 0
    for i in range(numOfCorrections):
        corDis, corAzm = tempList[i].split(',') 
        tempSum = tempSum + float(corDis) * sin(radians(convertStrToDegrees(corAzm))) 
    ewCorrection = tempSum / numOfCorrections
    
    presentLat = convertMinutesToStr((convertStrToMinutes(values['assumedLat']) + nsCorrection))
    presentLong = convertMinutesToStr((convertStrToMinutes(values['assumedLong']) + ewCorrection))
    
    tempSum = 0
    for i in range(numOfCorrections):
        corDis, corAzm = tempList[i].split(',') 
        tempSum = tempSum + sqrt(pow((float(corDis) * cos(radians(convertStrToDegrees(corAzm))) - nsCorrection), 2) + 
                                 pow((float(corDis) * sin(radians(convertStrToDegrees(corAzm))) - ewCorrection), 2))
    percision = float(1)/numOfCorrections * tempSum                         
    percision = myRound(percision)
                           
   
    
    values['percision'] = str(percision)
    
    
    
    
    
    
    

    return values;