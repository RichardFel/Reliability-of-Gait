# -*- coding: utf-8 -*-

'''
Created by R. Felius 27/08/2020 in collaboration with Hogeschool Utrecht,
Vrije universiteit Amsterdam, De Parkgraaf en de Hoogstraat Revalidatie.
Modified at 25/06/2021

This script is written to analyse data for the project: 
Making sense of sensor data for personalised healthcare.
This script can be used to analyse static postural balance.

The inputs are CSV files with 7 columns: Timestamp [0], IMU accelerometer [1,2,3] 
and gyroscope [4,5,6] data. See /Data for an example.

IMPORTANT:
- Set working directory
- Calculate gyroscope bias prior to measurement, see /Calibration/calibration.py

'''

import os
import sys

mainDirectory = os.getcwd()
sys.path.append(str(mainDirectory + '/calibration'))
sys.path.append(str(mainDirectory + '/Functions'))

from calibration import addCalibration
from calcgaitfeatures import calcFeatures
from calcICC import calculateICCMDC
import pythontolatex 
import gaitplot 

walking_aid =   (['with', 'without'])
rehabC =    (['P'])                                                           # Set availible rehabcentres
testTypes = (['Test'])                                                  # Testtype
nSubjects = 1                                                                  # Set number of participants
settings =  {'rehabC' : rehabC,
            'testTypes': testTypes,
            'nSubjects': nSubjects,
            'walking_aid':walking_aid
            }


def main():

    #    addCalibration.determineGyroscopeError(mainDirectory, verbose = True)    
    
    calcFeatures(settings, plotje = True, verbose = True)
#    calculateICCMDC()
#    meanStdtoLatex()    # Return Mean and STD in latex table format
#    iccmdctoLatex()     # Return Mean and STD in latex table format
#    mdcRawToLatex()     # Return Mean and STD in latex table format
#    plotgait()          # Creates figures 
    
if __name__ == "__main__":
    main()
