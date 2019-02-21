from cmath import sqrt

def adjust(values = None):
    
    dip = -0.97 * sqrt(int(values['height'])) / 60
    
    
    result = values
    return result