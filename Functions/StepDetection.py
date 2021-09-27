import numpy as np
import matplotlib.pyplot as plt
from scipy import signal   
from FrequencyFeatures import fastfourierTransform
from scipy import integrate
from scipy.stats import pearsonr
import Proces

def detectStepsFeet(sensors, plotje, verbose):
    leftfoot = sensors["leftfoot"]
    rightfoot = sensors["rightfoot"]
    differenceRL = stepdetectDifference(rightfoot, leftfoot,plotje, verbose, maxStrideFreq = 1)
    differenceLR = stepdetectDifference(leftfoot, rightfoot,plotje, verbose, maxStrideFreq = 1)
    for maxStrideFreq in range(1,3):
        if ((differenceRL <= differenceLR) &(differenceRL < 8)):
            _ = stepdetectDifference(rightfoot, leftfoot,plotje, verbose, maxStrideFreq)       
            if ((leftfoot.stridenum < 12) or(rightfoot.stridenum < 12) or
                (np.isnan(np.mean(np.diff(leftfoot.peaks)))) or 
                (np.isnan(np.mean(np.diff(rightfoot.peaks))))):
                continue
            else:
                break
        elif    ((differenceLR <= differenceRL) & (differenceLR < 8)):
            _ = stepdetectDifference(leftfoot, rightfoot,plotje, verbose, maxStrideFreq)
            if ((leftfoot.stridenum < 12) or(rightfoot.stridenum < 12) or
                (np.isnan(np.mean(np.diff(leftfoot.peaks)))) or 
                (np.isnan(np.mean(np.diff(rightfoot.peaks))))):
                continue
            else:
                break
        else:     
            continue

    if ((leftfoot.stridenum < 12) or(rightfoot.stridenum < 12) or
        (np.isnan(np.mean(np.diff(leftfoot.peaks)))) or 
        (np.isnan(np.mean(np.diff(rightfoot.peaks))))):
        raise Exception
    sensors["leftfoot"] = leftfoot
    sensors["rightfoot"] = rightfoot
    return sensors

def stepdetectDifference(firstFoot, secondFoot, plotje, verbose, maxStrideFreq):
    stepFrequency(firstFoot,maxStrideFreq, plotje)
    stepdetectionFoot(firstFoot, plotje, verbose)
    stepFrequency(secondFoot, firstFoot.fftsignalML.stridefreq, plotje)
    stepdetectionFoot(secondFoot, plotje, verbose)
    return np.abs(secondFoot.stridenum -firstFoot.stridenum)

def stepFrequency(self, maxStrideFreq, plotje = False):               
    self.accFT = np.array(self.acceleration)                                  
    self.fftsignalML = fastfourierTransform(self.acceleration[:,1], 
                                        direction = 'ML',
                                        sampleFreq = self.sampleFreq, 
                                        lineartaper = False, 
                                        plotje = False, 
                                        window = False,
                                        )
    self.fftsignalML.FFTGait(hzMax = maxStrideFreq, hzMin = 0.15)
    self.dominantFreq = ((1 / self.fftsignalML.stridefreq)/ self.sampleFreq)           
    self.accMag = Proces.magnitude(self.acceleration)
    self.gyrMag = Proces.magnitude(self.gyroscope)
    self.threshAcc = np.mean(self.accMag) + np.std(self.accMag) 
    self.threshGyr = np.mean(self.gyrMag) 
    threshT(self)

def threshT(self):
    if self.dominantFreq    < 100:          
        multiplyr       = 0.25
    elif self.dominantFreq  < 150:    
          multiplyr     = 0.3
    else :    
          multiplyr     = 0.4
    self.threshT            = int(np.floor(self.dominantFreq * multiplyr)) 
    self.threshT = min(self.threshT, 50)

def stepdetectionFoot(self, plotje = None, verbose = None):
    self.accVT = self.acceleration[:,2]
    self.height = np.mean(self.accVT[self.walkPart]) + np.std(self.accVT[self.walkPart])
    peaks = signal.find_peaks(self.accVT[self.walkPart], 
                                distance = int(self.dominantFreq * 0.75)  ,                   
                                height =  self.height)
    self.peaks = peaks[0] + self.walkPart[0]  
    self.difPeaks = np.concatenate((np.diff(self.peaks) , np.array([0])))
    falseNegative(self, verbose)
    falsePositive(self, verbose)
    swingphases(self)
    if plotje: 
        makeFigures(self)
    
def makeFigures(self):                                                     
    fig1, ax2 = plt.subplots(1, figsize = (25,15), dpi = 110)
    ax2.plot(np.array(range(len(self.accVT))) , self.accVT)
    ax2.plot(self.peaks, self.accVT[self.peaks],  'o')
    ax2.set_title('Two minute walking with peak detection')
    ax2.legend(['Left foot sensor'])
    ax2.set_ylabel("Acceleration VT [G]")
    ax2.set_xlabel("Time [s]")
    #        few_peaks = accVT[2000:3000]
    #        fig1, ax2 = plt.subplots(1, figsize = (25,15), dpi = 110)
    #        ax2.plot((np.array(range(0,len(few_peaks)))/100), 
    #                 few_peaks
    #                 )
    #        peak_points = peaks[np.where((peaks >= 2000) & (peaks <= 3000))]-2000
    #        ax2.plot(peak_points/100, 
    #                 few_peaks[peak_points],  
    #                 'o')          
    #        ax2.set_title('Two minute walking with peak detection')
    #        ax2.legend(['Left foot sensor'])
    #        ax2.set_ylabel("Acceleration VT [G]")
    #        ax2.set_xlabel("Time [s]")
    
def falseNegative(self, verbose):
    ''' Checks large gaps between foottouchers if there is definetly no foottouch 
    can be determined'''
    tmpPeaks = []
    for i in range(len(self.peaks)):
        tmpPeaks.append(self.peaks[i])
        if self.difPeaks[i] > (self.dominantFreq*1.5):
            try:
                tmpPeak = signal.find_peaks(self.accVT[self.peaks[i]+self.threshT:self.peaks[i+1]-self.threshT], 
                                            height = self.height*0.75)[0][0] + self.peaks[i]+self.threshT
                if (
                    tmpPeak - tmpPeaks[-1] >= self.threshT * 0.75
                    and self.peaks[i + 1] - tmpPeak >= self.threshT * 0.75
                ):
                    if verbose:
                        print(f'We added a peak at: {tmpPeak}')
                    tmpPeaks.append(tmpPeak)
            except IndexError: 
                pass
    self.peaks = np.array(tmpPeaks)  
    
def falsePositive(self, verbose): 
    ''' Used to find standphases between the peaks, if no standphase can be found
    the peak is defined as a false positive. 
    '''
    standphases = [np.arange(0, self.walkPart[0])]
    if standphases[0].size == 0:
        standphases[0] = np.array([0,1])
    for peak in range(len(self.peaks)-2):
        tmpThreshAcc = self.threshAcc / 2
        tmpThreshGyr = self.threshGyr / 2
        tmpThreshTime = self.threshT
        stationaryCount = []
        counter = 0
        try:
            for counter2 in range(8):
                for sample in range(self.peaks[peak],self.peaks[peak+1]):                       
                    if ((self.accMag[sample] < tmpThreshAcc) and (self.gyrMag[sample] < tmpThreshGyr)):       
                        stationaryCount.append(sample)                                                 
                        counter  += 1        
                        if ((sample == (self.peaks[peak+1]-1)) & (counter > self.threshT)): 
                            standphases.append(np.array(stationaryCount[:-1]))
                            break
                    elif (counter > self.threshT):
                        standphases.append(np.array(stationaryCount))
                        break
                    else:
                        counter = 0
                        stationaryCount   = []
                if counter > self.threshT:
                    break
                else:
                    tmpThreshAcc *= 1.2 
                    tmpThreshGyr *= 1.2
                    tmpThreshTime *= 0.7
                    
                if (counter2 == 7):
                    arr = np.array([self.peaks[peak], self.peaks[peak+1]])
                    delPeak = np.where(self.peaks == arr[np.where(self.accVT[arr] == np.min(self.accVT[arr]))[0]])[0]
                    if verbose:
                        print(f'We deleted a peak at: {delPeak}')
                    self.peaks = np.delete(self.peaks, delPeak)
                    break
        except IndexError:
            pass
    standphases.append(np.arange(self.walkPart[-1],len(self.accVT) ))
    self.standphases = standphases
    
def swingphases(self):
    swingphases = [
        np.array(range(self.standphases[i][-1], self.standphases[i + 1][0]))
        for i in range(len(self.standphases) - 1)
    ]
    self.swingphases = swingphases
    self.stridenum = len(swingphases) 
        
def stepdetectionLowback(sensors, per_N_steps, plotje, printje):
    filtedSignalAP = intFilt(sensors['lowback'])
    peaks = signal.find_peaks(filtedSignalAP[:500],
                            height = np.mean(filtedSignalAP[:500]) + (np.std(filtedSignalAP[:500])),                 
                            distance = int(sensors['leftfoot'].dominantFreq * 0.25)
                            )
    firstpeak = peaks[0][0]
    firstStepDirection(sensors['lowback'], firstpeak)
    detectStepsLowBack(sensors, filtedSignalAP, firstpeak)
    #    if plotje:
    #        fig1, ax2 = plt.subplots()
    #        ax2.plot(np.array(range(len(filtedSignalAP))), filtedSignalAP)
    #        ax2.plot(peaks, filtedSignalAP[peaks],'o') 
        
    
def detectStepsLowBack(sensors, filtedSignalAP, firstpeak):
    deviation = 15
    
    filtedSignalAP = np.concatenate((filtedSignalAP,np.zeros(1000)))
    for _ in range(4):
        deviation += 5
        if sensors['lowback'].firstStepDir == 'Right':
            stridesfirst, stridessecond = lowbacksteps(sensors, filtedSignalAP, firstpeak, deviation, 'rightfoot', 'leftfoot')       
        else:
            stridesfirst, stridessecond =lowbacksteps(sensors, filtedSignalAP, firstpeak, deviation, 'leftfoot', 'rightfoot')  
        peakslowback = np.concatenate((stridesfirst, stridessecond))
        peakslowback = np.delete(peakslowback, np.where(filtedSignalAP[peakslowback] == 0)[0])
        peakslowback = np.array(peakslowback[np.argsort(peakslowback)])

        if (np.abs(len(peakslowback) - (sensors['leftfoot'].stridenum + sensors['rightfoot'].stridenum)) < 10):
            break
        if sensors['lowback'].firstStepDir == 'Right':
            stridesfirst, stridessecond =lowbacksteps(sensors, filtedSignalAP, firstpeak, deviation, 'leftfoot', 'rightfoot')       
        else:
            stridesfirst, stridessecond = lowbacksteps(sensors, filtedSignalAP, firstpeak, deviation, 'rightfoot', 'leftfoot')  
        peakslowback = np.concatenate((stridesfirst, stridessecond))
        peakslowback = np.delete(peakslowback, np.where(filtedSignalAP[peakslowback] == 0)[0])
        peakslowback = np.array(peakslowback[np.argsort(peakslowback)])
        if (np.abs(len(peakslowback) - (sensors['leftfoot'].stridenum + sensors['rightfoot'].stridenum)) < 10):
            break

    sensors['lowback'].stridenum = len(peakslowback)
    sensors['lowback'].peaks = peakslowback

def lowbacksteps(sensors, filtedSignalAP, firstpeak, deviation, firstfoot, secondfoot):
    MinPeakDifference= int(sensors['leftfoot'].dominantFreq * 0.2)
    stridesfirst = detectStride(sensors[firstfoot].peaks, filtedSignalAP, firstpeak, deviation)         
    stridessecond = detectSecondFoot(sensors[secondfoot].peaks, filtedSignalAP, stridesfirst, MinPeakDifference, sensors[secondfoot].dominantFreq) 
    return stridesfirst, stridessecond

def detectStride(peaks, filtedSignalAP, firstpeak, deviation):
    peaks -= peaks[0] -  firstpeak
    peaksstridelowback = [peaks[0]]
    diffpeaks = np.diff(peaks)

    try:
        for j in range(len(peaks)-2):
            searchWindow = np.array(range(peaks[1]-deviation,peaks[1]+deviation))
            peaks[1] = (np.where(np.max(filtedSignalAP[searchWindow]) == filtedSignalAP[searchWindow])[0][0] + (peaks[1] - deviation) )
            peaksstridelowback.append(peaks[1])
            peaks[1] += diffpeaks[j+1]
    except IndexError:
        print('search window out of bound.')

    try:
        searchWindow = np.array(range(peaks[1]-deviation,peaks[1]+deviation))
        peaks[1] = (np.where(np.max(filtedSignalAP[searchWindow]) ==  filtedSignalAP[searchWindow])[0][0] +  (peaks[1] - deviation) )
        peaksstridelowback.append(peaks[1])
        peaksstridelowback = np.array(peaksstridelowback)
    except IndexError:
        print('search window out of bound, last step not found')

    return peaksstridelowback
    
def detectSecondFoot(peaks, filtedSignalAP, foundLowBackPeaks, MinPeakDifference, dominantFreq):
    peaksstridelowback = []

    try:
        for i in range(len(peaks)-1):  
            start = int(foundLowBackPeaks[i] + MinPeakDifference)
            stop = int(foundLowBackPeaks[i+1] - MinPeakDifference)
            peaksstridelowback.append(np.where(np.max(filtedSignalAP[start:stop])  == filtedSignalAP[start:stop])[0][0] + start)
    except (ValueError, IndexError):
        pass
    try:
        if len(peaksstridelowback) < len(peaks):
            difference = len(peaks) - len(peaksstridelowback)
            for _ in range(difference):
                start += int(dominantFreq)
                stop += int(dominantFreq) 
                peaksstridelowback.append(np.where(np.max(filtedSignalAP[start:stop])  == filtedSignalAP[start:stop])[0][0] + start)
    except ValueError: 
        pass
    return peaksstridelowback
        
def intFilt(self):
    filtAbove = self.fftsignalVT.stepfreq / 4
    accelerationORAP = self.accRotated[self.walkPart,0]
    ORAPInt = integrate.cumtrapz(accelerationORAP, accelerationORAP, self.sampleFreq, axis = 0)
    ORAPFilt = Proces.butterworthFilter(ORAPInt,  self.sampleFreq, filterType = 'bandpass', cutoff = [filtAbove,15], order =1) 
    ORAPfiltInt = integrate.cumtrapz(ORAPFilt, ORAPFilt, self.sampleFreq, axis = 0)
    return Proces.butterworthFilter(ORAPfiltInt,  self.sampleFreq, filterType = 'bandpass', cutoff = [filtAbove,15], order =1)

def firstStepDirection(self, firstpeak):
    filtedSignalML = Proces.butterworthFilter(self.accRotated[self.walkPart,1],self.sampleFreq, 
                                              filterType = 'lowpass', cutoff = 1.5, order =1)
    firststepdir = np.mean(filtedSignalML[np.arange(firstpeak-10, firstpeak+10)])
    direction = 'Right' if firststepdir < np.mean(filtedSignalML) else 'Left'
    self.firstStepDir = direction