from math import sqrt, tan, pi

def adjust(values = None): 
    d, m =  values['observation'].split('d')
    degrees = float(d) + float(m) / 60
    radians = float(degrees * pi / 180)
    height = int(values['height'])
    temperature = int(values['temperature'])
    pressure = int(values['pressure'])
 
    dip = -0.97 * sqrt(height) / 60   
    refraction = (-0.00452 * pressure) / (273 + (temperature-32) * 5 / 9) / tan(radians)
    altitude = degrees + dip + refraction
    x = int(altitude)
    y = round(altitude % 1 * 60, 1)
    altitude = str(x) + 'd' + str(y) 
    values['altitude'] = altitude
    
    result = values
    return result