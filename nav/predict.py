from math import sqrt, tan, pi
import xlrd

def predict(values = None):
    
    
    
    workbook = xlrd.open_workbook('C:\Users\Angus\Desktop\stardata.xlsx')
    sheet = workbook.sheet_by_index(0)
    sheet.cell_value(0, 0)
    result = 'not found'
    for i in range(sheet.nrows):
        if (sheet.cell_value(i, 0) == values['body']):
            result = 'found'
    
    return result