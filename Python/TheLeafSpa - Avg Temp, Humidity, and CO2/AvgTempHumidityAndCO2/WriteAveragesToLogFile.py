'''
Created on Mar 8, 2017

@author: margaret
'''
import csv
def writeAveragesToLogFile(logFile,averages):
    rowToWrite = []
    with open(logFile, 'ab') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow(['Average Values'])
        writer.writerow(['LED ON',' ',' ','LED OFF'])
        writer.writerow(['Temp','Humidity','CO2','Temp','Humidity','CO2'])
        for index, values in enumerate(averages):
            for i, elem in enumerate(values):
                try:
                    rowToWrite[i] =  str(rowToWrite[i])+','+str(elem)
                except:
                    rowToWrite.append(elem)
        for index in enumerate(averages):
            for i, value in enumerate(index):
                #see http://stackoverflow.com/questions/12240662/write-list-of-comma-separate-strings-to-csv-file-in-python
                writer.writerow(rowToWrite[i].split(','))
            break;