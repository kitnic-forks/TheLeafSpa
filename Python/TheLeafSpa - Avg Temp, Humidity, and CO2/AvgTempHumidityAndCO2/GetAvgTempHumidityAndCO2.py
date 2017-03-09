'''
Created on Mar 8, 2017

@author: margaret
'''
# Assumes log file is in Settings_V1 format.  If the first column contains:  
# - 51 -> start or stop analyzing data.  Stop analyzing happens in the case
#   where there are multiple rows with 51 in the first column.  This means
#   the firmware was restarted.
#  - 0 ->  The row contains readings for Temp, humidity, and CO2
#  - 3 ->  The LEDs are turned ON
#  - 4 ->  The LEDs are turned OFF
# 
import sys
import csv
import logging
logger = logging.getLogger(__name__)

def getAverage(listOfValues,index):
    if len(listOfValues) > 0:
        avg = sum(listOfValues)/float(len(listOfValues))
    else:
        avg = None
    return avg
#
# Returns the average values as a list of lists: [ [results for first run],
# [results for second run]...]
# results list:
# Average temp when LED is ON
# Average humidity when LED is ON
# Average CO2 when LED is ON
# Average temp when LED is OFF
# Average humidity when LED is OFF
# Average CO2 when LED is OFF
def getAvgTempHumidityAndCO2(logFile):
    logger.debug('at beginning of getAvgTempHumidityAndCO2....')
    # 
    # Read a row in the file.  If the first element is not an integer, exit
    # because this isn't a log file.
    with logFile as csvfile:  #the log file is a CSV file
        csvReader = csv.DictReader(csvfile,fieldnames=('rowType','date','time','temp','humidity','CO2'))
        for row in csvReader:  
            # if the 'rowType' is not an integer, exit
            rowType = int(row['rowType'])
            if not isinstance(rowType,int):
                logger.error('The first column in the log file holds an integer representing the row type')
                sys.exit()
            # looking for a row type of 51 (start of data capture for a session)
            inDataCaptureState = False
            if rowType == 51:
                break; 
        # row type is 51, so now loop through until next 51
        inDataCaptureState = True
        # First 3 lists are for temp,humidity,CO2 when LED is ON.
        # Second 3 for when LED is OFF.
        listOfValues = [[],[],[],[],[],[]]
        listOfAverages = [[],[],[],[],[],[]]
        for dataCaptureRow in csvReader:   
            # if the 'rowType' is not an integer, exit
            try:
                rowType = int(dataCaptureRow['rowType'])
            except:
                logger.error('Error - the row type: *%s* is not valid. Bye Bye.'%rowType)
                sys.exit()                    
            if rowType == 3: #LED is turned on
                inLEDonState = True
            if rowType == 4: # LED is turned off
                inLEDonState = False
            if rowType == 0: # A reading
                temp = float(dataCaptureRow['temp'])
                humidity = float(dataCaptureRow['humidity'])
                CO2 = float(dataCaptureRow['CO2'])
                if inLEDonState:
                    listOfValues[0].append(temp)
                    listOfValues[1].append(humidity)
                    listOfValues[2].append(CO2)
                else:
                    listOfValues[3].append(temp)
                    listOfValues[4].append(humidity)
                    listOfValues[5].append(CO2)
            if rowType == 51: # end of a capture.  Put averages into a list of lists
                i=0
                for values in listOfValues:
                    avgValue = getAverage(values,i)
                    listOfAverages[i].append(avgValue)
                    i+=1
                listOfValues = [[],[],[],[],[],[]]
        # gone through all rows...
        i=0
        for values in listOfValues:
            avgValue = getAverage(values,i)
            listOfAverages[i].append(avgValue)
            i+=1
        return listOfAverages
    
 