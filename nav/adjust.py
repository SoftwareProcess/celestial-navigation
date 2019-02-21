from math import sqrt, tan, pi

def adjust(values = None):
    
    degree, minut =  values['observation'].split('d')
    minutes = float(degree) + float(minut) / 60
    radians = float(minutes * pi / 180)
    height = int(values['height'])
    temperature = int(values['temperature'])
    pressure = int(values['pressure'])
    
    
    
    dip = -0.97 * sqrt(height) / 60   
    refraction = (-0.00452 * pressure) / (273 + (temperature-32) * 5 / 9) / tan(radians)
    
    
    result = refraction.real
    return result