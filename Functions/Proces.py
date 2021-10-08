import numpy as np
from scipy import signal
import Visualise

def dataPreperation(sensors, plotje, verbose):
    startEnd(sensors['leftfoot'], 'foot', minDiff = 10000,maxDiff = 13000)
    startEnd(sensors['rightfoot'], 'foot',minDiff = 10000,maxDiff = 13000)
    startEnd(sensors['lowback'] , 'lowback', minDiff = 10000,maxDiff = 13500)
    bruijn_rotation(sensors['lowback'],plotje = plotje)   
    if verbose:
        print(f' included signal length leftfoot {len(sensors["leftfoot"].walkPart)}')
        print(f' included signal length rightfoot {len(sensors["rightfoot"].walkPart)}')
        print(f' included signal length lowback {len(sensors["lowback"].walkPart)}')
        print('\n checkpoint 1 passed \n')
    return sensors

def magnitude(signal):                                                         
    return np.sqrt(np.sum(signal * signal, axis = 1))

def butterworthFilter(inputSignal,  sampleFreq, filterType, cutoff, order =1):
    filtAcceleration = np.zeros(len(inputSignal))
    if filterType == 'bandpass':
        b, a = signal.butter(order,[(2*cutoff[0])/(1/sampleFreq),
                                     (2*cutoff[1])/(1/sampleFreq)], btype = filterType)
    else:
        b, a = signal.butter(order,(2*cutoff)/(1/sampleFreq), btype = filterType)
    filtAcceleration = signal.filtfilt(b,a, inputSignal)
    return filtAcceleration
    
def rotsig(signal, rotmatrix):
    x = ( signal[:,0] * rotmatrix[0,0]) + ( signal[:,0] * rotmatrix[0,1])
    y = ( signal[:,1] * rotmatrix[1,0]) + ( signal[:,1] * rotmatrix[1,1])
    z = signal[:,2]
    return np.transpose(np.array((x,y,z)))

def bruijn_rotation(self, plotje = None):
    meanAcceleration = np.mean(self.acceleration,axis = 0)
    x_tmp=np.array([0, 0, 1])
    y=np.cross(meanAcceleration,x_tmp)
    x=np.cross(y,meanAcceleration)
    normx=x/np.linalg.norm(x)
    normy=y/np.linalg.norm(y)
    normz= meanAcceleration / np.linalg.norm(meanAcceleration)
    R=np.array((normx.transpose(), normy.transpose(), normz.transpose()))
    self.accRotated=(R.transpose().dot(self.acceleration.transpose())).transpose()
    self.gyrRotated =(R.transpose().dot(self.gyroscope.transpose())).transpose()
    if plotje:
        Visualise.plot1(self.accRotated, 'Acceleration VT, ML, AP', 'Samples', 'Acceleration [G]')
        Visualise.plot1(self.gyrRotated, 'Gyroscope VT, ML, AP', 'Samples', 'Angular velocity [deg/s]')

def threshold(sensorPos,gyrMag):
    if sensorPos == 'foot':
        return np.mean(gyrMag)
    else:
        return np.mean(gyrMag) + np.std(gyrMag) * 0.2

def detectStandphases(accMag, gyrMag, threshAcc,threshGyr):
    standphases = []
    tmpCounter = 0
    for (counter, value) in enumerate(accMag):  
        if value < threshAcc and gyrMag[counter] < threshGyr:  
            tmpCounter += 1  
        else:
            if tmpCounter > 30:
                standphases.append(np.array(range(counter - tmpCounter,
                                   counter)))
            tmpCounter = 0
        if (value == accMag[-1]) & (tmpCounter > 0):
            standphases.append(np.array(range(counter - tmpCounter,
                               counter)))
    return standphases

def beginEnd(standphases, minDiff, maxDiff):
    # Signal should include at least 25 standphases
    Begin =[len(i) for i in standphases[0:25]]
    End = [len(i) for i in standphases[-25:len(standphases)]]
    sortBegin = np.sort(Begin)[::-1]
    sortEnd = np.sort(End)[::-1]
    for start in sortBegin:
        startArray = standphases[np.where(Begin== start)[0][0]]
        for end in sortEnd:
            endArray = standphases[np.where(End== end)[0][0] - 25 + len(standphases)]
            sampeDiff = len(np.arange(startArray[-1],endArray[0]))
            if ((sampeDiff > minDiff) & (sampeDiff < maxDiff)):
                return startArray, endArray

def walksig(self, startArray, endArray):
    beginSample = startArray[-1] - 100 if len(startArray) > 100 else 0
    if len(endArray) > 100:
        endSample = endArray[0] + 100
    else:
        endSample = len(self.acceleration) - 1
    self.walkPart = np.arange(beginSample, endSample)
    
def startEnd(self,sensorPos,minDiff,maxDiff,):
    accMag = magnitude(self.acceleration)
    gyrMag = magnitude(self.gyroscope)

    # thresholds
    threshAcc = np.mean(accMag) + np.std(accMag)
    threshGyr = threshold(sensorPos,gyrMag)

    # Detect stationairy periods in the signal
    standphases = detectStandphases(accMag, gyrMag, threshAcc,threshGyr)
    startArray, endArray = beginEnd(standphases, minDiff, maxDiff)

    # Find the most likely start and end of the signal
    walksig(self, startArray, endArray)

def resample(self, n_strides, firststride, new_sf, input_signal):
    laststride = firststride + n_strides
    begin = int((self.peaks[firststride-1] + self.peaks[firststride]) / 2)
    end = int((self.peaks[laststride-1] + self.peaks[laststride]) / 2)
    n_samples = n_strides * new_sf
    self.resampled = np.zeros((n_samples,3))
    for i in range(3):
        resamp_signal = input_signal[begin:end,i]
        y_new = np.zeros(n_samples)
        f = signal.decimate(resamp_signal, 2)
        y_new = signal.resample(f, n_samples)
        self.resampled[:,i] = y_new

