from math import cos 
from math import radians 
from math import sin 
from math import sqrt 
from math import pow
import ast


def locate(values = None):

    def validate(arg, lowerBound, upperBound, condition):
        if ('d' not in arg):
            return False
        x, y = arg.split('d')
        if (x == ''):
            return False
        x = x.lstrip('0')
        if (x == ''):
            x = '0'
        y = y.lstrip('0')
        if (y == ''):
            y = '0'       
        try:
            y = int(y)
        except ValueError:  
            pass     
        else:
            return False
        try:
            if (condition == 'ge'):    
                if (int(x) < lowerBound or int(x) >= upperBound or float(y) < 0.0 or float(y) >= 60.0):
                    return False  
            if (condition == 'gt'):
                if (int(x) <= lowerBound or int(x) >= upperBound or float(y) < 0.0 or float(y) >= 60.0):
                    return False
        except ValueError:
            return False                 
        y = str(float(y)).zfill(1) 
        return True

    
    
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
 
# validate parameters
    if (not(values.has_key('assumedLat')) or values['assumedLat'] == ''):
        values['error'] = 'mandatory information is missing'
        return values
    if (validate(values['assumedLat'], -90, 90, 'gt') == False):
        values['error'] = 'assumedLat is not valid'
        return values 
    if (not(values.has_key('assumedLong')) or values['assumedLong'] == ''):
        values['error'] = 'mandatory information is missing'
        return values
    if (validate(values['assumedLong'], 0, 360, 'ge') == False):
        values['error'] = 'assumedLong is not valid'
        return values
    if (values['assumedLong'][0] == "-"):
        values['error'] = 'assumedLong is not valid'
        return values    
    if (not(values.has_key('corrections')) or values['corrections'] == ''):
        values['error'] = 'mandatory information is missing'
        return values 

    
 
    correctionString = values['corrections']
    if (correctionString.startswith('[') and correctionString.endswith(']')):
        correctionString = correctionString[1:-1]
    else:
        values['error'] = 'correction is not valid'
        return values
    if (correctionString.count('[') != correctionString.count(']')):
        values['error'] = 'correction is not valid'
        return values
    if (correctionString.count('[') == 0 or correctionString.count(']') == 0):
        values['error'] = 'correction is not valid'
        return values
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
    try:
        for i in range(numOfCorrections):
            corDis, corAzm = tempList[i].split(',') 
            if (validate(corAzm, 0, 360, 'ge') == False):
                values['error'] = 'correction is not valid'
                return values
            if (corAzm[0] == '-'):
                values['error'] = 'correction is not valid'
                return values
            tempSum = tempSum + float(corDis) * cos(radians(convertStrToDegrees(corAzm)))
    except:
        values['error'] = 'correction is not valid'
        return values 
    
    
#     for i in range(numOfCorrections):
#         corDis, corAzm = tempList[i].split(',') 
#         if (validate(corAzm, 0, 360, 'ge') == False):
#             values['error'] = 'correction is not valid4'
#             return values
#         if (corAzm[0] == '-'):
#             values['error'] = 'correction is not valid5'
#             return values
#         tempSum = tempSum + float(corDis) * cos(radians(convertStrToDegrees(corAzm)))
       
    
    
    
    
    
    
    
    nsCorrection = tempSum / numOfCorrections
    
    tempSum = 0
    for i in range(numOfCorrections):
        corDis, corAzm = tempList[i].split(',') 
        tempSum = tempSum + float(corDis) * sin(radians(convertStrToDegrees(corAzm))) 
    ewCorrection = tempSum / numOfCorrections
    
    presentLat = convertMinutesToStr((convertStrToMinutes(values['assumedLat']) + nsCorrection))
    presentLong = convertMinutesToStr((convertStrToMinutes(values['assumedLong']) + ewCorrection))
    values['presentLat'] = presentLat
    values['presentLong'] = presentLong
    
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
    if (ptsList == None):
        values['accuracy'] = 'NA'
    else:
        temp = 0.0
        for i in range(len(ptsList)):
            if (i == len(ptsList) - 1):
                temp = temp + ptsList[i][0] * ptsList[0][1] - ptsList[i][1] * ptsList[0][0]
            else:
                temp = temp + ptsList[i][0] * ptsList[i+1][1] - ptsList[i][1] * ptsList[i+1][0]
        accuracy = myRound(temp / 2)
        values['accuracy'] = str(accuracy)
    
    
    return values;