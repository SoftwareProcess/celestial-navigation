from math import cos 
from math import radians 
from math import sin 
from math import sqrt 
from math import pow



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
 
    def convex_hull(points):
        points = sorted(set(points))
        if len(points) < 3:
            return None
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
 
        return lower[:-1] + upper[:-1]
 
 
 
 
 
 
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
# Percision    
    tempSum = 0
    for i in range(numOfCorrections):
        corDis, corAzm = tempList[i].split(',') 
        tempSum = tempSum + sqrt(pow((float(corDis) * cos(radians(convertStrToDegrees(corAzm))) - nsCorrection), 2) + 
                                 pow((float(corDis) * sin(radians(convertStrToDegrees(corAzm))) - ewCorrection), 2))
    percision = float(1)/numOfCorrections * tempSum                         
    percision = myRound(percision)
    values['percision'] = str(percision)
    
# Accuracy        
    pts = []   
    for i in range(numOfCorrections):
        corDis, corAzm = tempList[i].split(',') 
        pts += [[0.0]*2]
        pts[i][0] = float(corDis) * float(cos(radians(convertStrToDegrees(corAzm))))
        pts[i][1] = float(corDis) * float(sin(radians(convertStrToDegrees(corAzm))))
        pts[i] = tuple(pts[i])
    ptsList = convex_hull(pts)
    
    temp = 0.0
    for i in range(len(ptsList)):
        if (i == len(ptsList) - 1):
            temp = temp + ptsList[i][0] * ptsList[0][1] - ptsList[i][1] * ptsList[0][0]
        else:
            temp = temp + ptsList[i][0] * ptsList[i+1][1] - ptsList[i][1] * ptsList[i+1][0]
    accuracy = myRound(temp / 2)
    
    
    
    return accuracy;