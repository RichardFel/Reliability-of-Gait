import os
import sys

import numpy as np

mainDirectory = '/Users/richard/Library/Mobile Documents/com~apple~CloudDocs/Desktop/PhD/Algorithms PhD/Beroerte/Reliability of Gait'
os.chdir(mainDirectory)
sys.path.append(str(mainDirectory + '/Functions'))
import SaveResults 
import SpatioTemporalFeatures
import ComplexityFeatures
import FrequencyFeatures
import AsymmetryFeatures
import Proces
from LoadFiles import loadCsv     

def calcFeatures(subject, testType, plotje = None, verbose = None):
    results =  SaveResults.saveresults()                                    
    results = procesData(subject, testType, results, plotje, verbose)   
    results.to_excel('gait_features.xlsx',)   
    if verbose:
        print('/Results/Results saved')

def calcFeaturesmakingsense(settings, plotje = None, verbose = None):
    results =  SaveResults.saveresults()                                    
    results = procesDataMkingSense(settings, results, plotje,verbose)       
    results.to_excel(mainDirectory + '/Results/gait_features.xlsx',)  
    if verbose:
        print('Results saved')

def procesData(subject, testType, results, plotje, verbose):
    resample = True
    makingsense = False
    sensors = readData(plotje, resample,makingsense)
    outcomes = Analyse(sensors, plotje, verbose)         
    results = SaveResults.updatedataframe(results, subject, testType,outcomes)
    return results

def procesDataMkingSense(settings, results, plotje, verbose):
    resample = True
    makingSense = True
    for RevC in settings['rehabC']:                                                     
        for nSubject in range(1,settings['nSubjects']+1):
            subject = 'S' + str(nSubject).zfill(3) + RevC
            for aid in settings['walkingAid']:     
                for testType in settings['testTypes']:                          
                    locInExcel = 11
                    if testType == 'Hertest':
                        locInExcel += 19
                    if aid ==  'without':
                         locInExcel += 1
                    try:
                        sensors = readData(plotje, resample, makingSense, locInExcel, subject, testType)
                        sensors, asymmetryResults = Analyse(sensors, plotje, verbose)         
                        results = SaveResults.updatedataframe(results,subject, testType, sensors, asymmetryResults)
                    except (FileNotFoundError) as e: 
                        print(e)
    return results
            
def readData(plotje,resample,makingSense, locInExcel=None,subject=None,testType=None,):
    leftFoot = loadCsv(owd=mainDirectory,fileName='leftfoot.csv',plotje = plotje,
                       resample = resample, makingSense = makingSense,
                       locInExcel = locInExcel,subject = subject,
                       testType = testType)
    rightFoot = loadCsv(owd=mainDirectory,fileName='rightfoot.csv',plotje = plotje,
                       resample = resample, makingSense = makingSense,
                       locInExcel = locInExcel,subject = subject,
                       testType = testType)
    lowBack = loadCsv(owd=mainDirectory,fileName='lowback.csv',plotje = plotje,
                       resample = resample, makingSense = makingSense,
                       locInExcel = locInExcel,subject = subject,
                       testType = testType)
    return {'leftfoot': leftFoot, 'rightfoot': rightFoot,'lowback': lowBack}

def Analyse(sensors, plotje, verbose):   
    sensors = Proces.dataPreperation(sensors, plotje, verbose)
    sensors = SpatioTemporalFeatures.calcFeaturesFeet(sensors, plotje, verbose, per_N_strides = 10)
    sensors = FrequencyFeatures.calcFeatures(sensors, plotje)
    sensors = SpatioTemporalFeatures.calcFeaturesLowback(sensors, plotje, verbose,  per_N_steps = 20)
    sensors = ComplexityFeatures.calcFeatures(sensors, plotje, verbose)
    asymmetryResults = AsymmetryFeatures.calcFeatures(sensors)
    return sensors, asymmetryResults

