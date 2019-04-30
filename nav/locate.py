from math import cos, radians, sin


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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return presentLat;