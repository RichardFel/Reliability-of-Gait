'''
Use this script to calculate the gyroscope bias.
The calibration files per sensor are stored in /calibrationFiles named 
according to the sensorID. Make sure to collect at least 15 minutes of 
stationary data to ensure correct gyroscope error estimation. 
'''


import os

import pandas as pd
import numpy as np


def getGyroscopeError(serialnumber):
    try:
        workingDirectory = os.getcwd()
        ccalibrationDirectory = workingDirectory + '/calibration'
        os.chdir(ccalibrationDirectory)
        gyorscopeErrorDF = pd.read_pickle('gyorscopeErrorDF.pkl')
        gyrx, gyry, gyrz = gyorscopeErrorDF.loc[serialnumber]
        return gyrx, gyry, gyrz
    except KeyError:
        print('Please make a calibration file using add_calibration and add the',
              'file to test_files/calib')
    finally:
        os.chdir(workingDirectory)
        

def determineGyroscopeError(workingDirectory = None, verbose = None):
    if workingDirectory == None:
        calibrationDirectory = os.getcwd()
    else:
        calibrationDirectory = workingDirectory + '/calibration'
        
    fileFolder = calibrationDirectory + '/calibrationFiles'
        
    for file in os.listdir(fileFolder):
        os.chdir(fileFolder)
        if file == '.DS_Store' :
            continue  
        if verbose:
            print(file)
            
        serialsensor1 = pd.read_csv(file, nrows = 1).loc[0][0] # voorkant schoen
        data = pd.read_csv(file,
                           header = 0,    
                           names = ['gx', 'gy', 'gz'], 
                           skiprows = 9, 
                           usecols = [4,5,6],
                           sep = ',',
                           error_bad_lines = False)
        data.dropna(how = 'any',inplace = True)       
        
        for i in range(3):  
            data.iloc[:,i] = pd.to_numeric(data.iloc[:,i],errors='coerce')

        gyroscope = np.radians(np.array(data.iloc[200:len(data)-200,:]))
        gyroscopeError = np.mean(gyroscope[0:len(data)-100,:],axis = 0)
            
        os.chdir(calibrationDirectory)
        gyorscopeErrorDF    = pd.read_csv('gyorscopeErrorDF.csv', index_col = 0)
        
        tempDF =   pd.DataFrame(data = [[gyroscopeError[0],gyroscopeError[1],
                                       gyroscopeError[2]]],
                                columns = ['gyrE1', 'gyrE2', 'gyrE3'], 
                                index = [serialsensor1])
        try:
            gyorscopeErrorDF = gyorscopeErrorDF.append(tempDF, verify_integrity = True)
            if verbose: 
                print('New Value added')
        except ValueError:
            if verbose:
                print('Value overwritten!')
            gyorscopeErrorDF.drop(index = serialsensor1, inplace = True)
            gyorscopeErrorDF = gyorscopeErrorDF.append(tempDF, verify_integrity = True)

        gyorscopeErrorDF.to_csv('gyorscopeErrorDF.csv')
    
    if workingDirectory == None:
        os.chdir(calibrationDirectory)
    else: 
        os.chdir(workingDirectory)
        
    if verbose:
         print('Gyroscope error of all known sensors succesfully computed')


if __name__ == "__main__":
    determineGyroscopeError(verbose = True)



