import csv
from datetime import datetime
import os.path

def predict(values = None):
    
    if (not(values.has_key('body'))):
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
        
    def convertStrToMinutes(arg):
        x, y = arg.split('d')
        minutes = int(x) * 60 + float(y)
        return minutes
    
    def convertMinutesToStr(arg):
        degree = int(arg / 60)
        minutes = round(arg % 60, 1)
        string = str(degree) + 'd' + str(minutes)
        return string
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "stardata.csv")
    found = False
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if (row[0].lower() == values['body'].lower()):
                SHA = row[1]
                dec = row[2]
                found = True
              
    if (not(found)):
        values['error'] = 'star not in catalog'
        return values
    
    values['lat'] = dec
       
    dateTime = date + ' ' + time
    try:
        dt = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        values['error'] = 'invalid date'
        return values;
    if (int(dt.year) < 2001 or int(dt.year) > 2100):
        values['error'] = 'invalid date'
        return values

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
    
    return values