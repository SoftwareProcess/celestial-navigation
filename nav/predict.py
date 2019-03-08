from math import sqrt, tan, pi
import xlrd
from datetime import datetime

def predict(values = None):
    
    def convertStrToMinutes(arg):
        x, y = arg.split('d')
        minutes = int(x) * 60 + float(y)
        return minutes
    
    def convertMinutesToStr(arg):
        degree = int(arg / 60)
        minutes = round(arg % 60, 1)
        string = str(degree) + 'd' + str(minutes)
        return string
    
    workbook = xlrd.open_workbook('C:\Users\Angus\Desktop\stardata.xlsx')
    sheet = workbook.sheet_by_index(0)
    sheet.cell_value(0, 0)
    result = 'not found'
    for i in range(sheet.nrows):
        if (sheet.cell_value(i, 0) == values['body']):
            SHA = sheet.cell_value(i, 1)
            dec = sheet.cell_value(i, 2)
    values['lat'] = dec
       
    dateTime = values['date'] + ' ' + values['time']
    dt = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
  
    yearDiff = int(dt.year) - 2001
    cumProgression = yearDiff * -14.31667
    
    count = 0
    for i in range (2001, int(dt.year)):
        if i % 4 == 0:
            count += 1
    dailyRotation = abs((1 - 86164.1/86400) * 60 * 360)    
    leapProgression = dailyRotation * count
   
    referenceDate = datetime(int(dt.year),01,01,0,0,0)
    seconds = (dt - referenceDate).total_seconds()
    rotation = (seconds / 86164.1) % 1 * 360 * 60
    
    GHAaries = 6042.6 + cumProgression + leapProgression + rotation
    
    GHAstar = GHAaries + convertStrToMinutes(SHA)
    GHAstar = GHAstar % (360 * 60)
    values['long'] = convertMinutesToStr(GHAstar)
    
    return GHAstar