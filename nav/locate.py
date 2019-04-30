

def locate(values = None):
    
    
    
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
    
    
    return numOfCorrections;