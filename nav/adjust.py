from cmath import sqrt, atan, pi

def adjust(values = None):
    
    degree, minut =  values['observation'].split('d')
    minutes = minut + degree * 60
    radians = minutes * pi / (60 * 180)
    height = float(values['height'])
    temperature = int(values['temperature'])
    pressure = int(values['pressure'])
    
    
    
    dip = -0.97 * sqrt(height) / 60   
    refraction = (-0.00452 * pressure) / (273 + (temperature-32) * 5 / 9) / atan(radians)
    
    
    result = refraction
    return result