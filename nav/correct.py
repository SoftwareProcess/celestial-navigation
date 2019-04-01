import csv
from datetime import datetime
import os.path
import re

def predict(values = None):
#check parameters   
    if (not(values.has_key('body')) or values['body'] == ''):
        values['error'] = 'body is missing'
        return values
    if (not(values.has_key('date'))):
        date = '2001-01-01'
    else:
        date = values['date']
    if (not(values.has_key('time'))):
        time = '00:00:00'
    else:
        time = values['time']    
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
#read data from csv
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "stardata.csv")
    found = False
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if (row[0].lower() == values['body'].lower()):
                SHA = row[1]
                dec = row[2]
                values['body'] = row[0]
                found = True            
    if (not(found)):
        values['error'] = 'star not in catalog'
        return values
#check if date and time is valid   
    dateform = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    if not dateform.match(date):
        values['error'] = 'date and time must have two digits'
        return values;
    timeform = re.compile("^[0-9]{2}:[0-9]{2}:[0-9]{2}$")
    if not timeform.match(time):
        values['error'] = 'date and time must have two digits'
        return values;


    dateTime = date + ' ' + time
  
    try:
        dt = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        values['error'] = 'invalid date'
        return values;
    if (int(dt.year) < 2001 or int(dt.year) > 2100):
        values['error'] = 'invalid date'
        return values
#calculate cum progression
    yearDiff = int(dt.year) - 2001
    cumProgression = yearDiff * -14.31667
#calculate leap progression    
    count = 0
    for i in range (2001, int(dt.year)):
        if i % 4 == 0:
            count += 1
    dailyRotation = abs((1 - 86164.1/86400) * 60 * 360)    
    leapProgression = dailyRotation * count
#calculate rotation   
    referenceDate = datetime(int(dt.year),01,01,0,0,0)
    seconds = (dt - referenceDate).total_seconds()
    rotation = (seconds / 86164.1) % 1 * 360 * 60
    
    GHAaries = 6042.6 + cumProgression + leapProgression + rotation   
    GHAstar = GHAaries + convertStrToMinutes(SHA)
    GHAstar = GHAstar % (360 * 60)
    
    values['long'] = convertMinutesToStr(GHAstar)
    values['lat'] = dec
    
    return values