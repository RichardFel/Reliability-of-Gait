import numpy as np
import Visualise

def calcFeatures(sensors, plotje):
   sensors['lowback'].accFT = np.array(sensors['lowback'].accRotated[sensors['lowback'].walkPart,:])
   sensors['lowback'].fftsignalML = fastfourierTransform(sensors['lowback'].accRotated[:,1],'ML', sensors['lowback'].sampleFreq,plotje)
   sensors['lowback'].fftsignalML.FFTGait(hzMax = 1.5, hzMin = 0.2, verbose = False)
   sensors['lowback'].fftsignalAP = fastfourierTransform(sensors['lowback'].accRotated[:,0],'AP', sensors['lowback'].sampleFreq,plotje)
   sensors['lowback'].fftsignalAP.FFTGait(hzMax = sensors['lowback'].fftsignalML.hzMax , hzMin = sensors['lowback'].fftsignalML.hzMin, verbose = False)
   sensors['lowback'].fftsignalVT = fastfourierTransform(sensors['lowback'].accRotated[:,2],'VT', sensors['lowback'].sampleFreq,plotje)
   sensors['lowback'].fftsignalVT.FFTGait(hzMax = sensors['lowback'].fftsignalML.hzMax , hzMin = sensors['lowback'].fftsignalML.hzMin,verbose = False)
   sensors['lowback'].dominantFreq = ((1 / sensors['lowback'].fftsignalML.stridefreq)/ sensors['lowback'].sampleFreq)    
   return sensors

class fastfourierTransform:
    def __init__(self, signal, direction, sampleFreq, lineartaper = None, 
                 plotje = None, window = None, ):
        self.signal = (signal - signal.mean()) / signal.std()
        self.signalLength = len(signal)                
        self.direction = direction
        if lineartaper :
            self.linearTaper()
        self.addZeros()
        self.window()
        fftsignal = np.fft.fft(self.signal * self.w)
        freqenties = np.fft.fftfreq(len(self.signal), sampleFreq)
        power = (abs(fftsignal) / len(self.signal))
        mask = freqenties > 0
        self.freqs = freqenties
        self.power = power
        self.fftTime = freqenties[mask]
        self.fftValues = power[mask]
        if plotje:
            Visualise.plot6(freqenties[mask], power[mask], title = 'Spectral Density plot ML',
                            xlabel = 'Frequency [Hz]',ylabel = 'Power',ylim = True)

    def linearTaper(self):
        self.signal[0:int(self.signalLength * 0.05 )] = (self.signal[0:int(self.signalLength * 0.05 )] / 20)
        self.signal[self.signalLength - int(self.signalLength * 0.05): self.signalLength ] = self.signal[self.signalLength - int(self.signalLength * 0.05): self.signalLength ] / 20

    def addZeros(self):
        check = True
        zeroscounter = 512
        while check:
            if (self.signalLength > zeroscounter):
                zeroscounter *= 2
            else:
                tot = zeroscounter - self.signalLength
                check = False
        self.signal = np.concatenate([self.signal, np.zeros(tot)]) 

    def window(self):
        if self.window == 'Hanning':
            self.w = np.hanning(len(self.signal)) 
        elif self.window == 'Hamming':
            self.w = np.hamming(len(self.signal))  
        else:
            self.w = 1
            
    def FFTGait(self, hzMax, hzMin, verbose = None):
        self.inphase(hzMax, hzMin)
        self.outphase(hzMax, hzMin)
        self.width()
        self.slope()
        self.density()
        self.harmonicratio = sum(self.inphase [:,0]) / sum(self.outphase [:,0]) 
        self.harmonicindex = self.inphase [0,0] / sum(self.inphase [0:5,0])
        self.dominantpeak = self.inphase [0,0]
        self.hzMax = self.inphase [0][2] * 2 + 1                         
        if self.direction == 'ML':
            self.stridefreq = self.inphase[0][2]
            self.hzMin = self.stridefreq + 0.5 * self.stridefreq 
        else :
            self.stepfreq = self.inphase[0][2]
        if verbose:
            self.printje()
            
    def inphase(self, hzMax, hzMin):   
        dominantFreqInphase = np.empty((9,3),float)
        frequencyRange = np.where((self.fftTime < hzMax) & (self.fftTime > hzMin))
        maxOfRange = max(self.fftValues[frequencyRange])
        result = np.where(maxOfRange == self.fftValues)
        hzOfMaxValue = self.fftTime[result[0][0]]
        dominantFreqInphase[0,0:3] = [maxOfRange, result[0][0], hzOfMaxValue]
        dominantfreqvalues = np.empty((8,20), int)
        for i in range(2,10):
            if (hzMax > 1.5):
                var = np.array(
                    range(
                        int(dominantFreqInphase[0][1]) * i - 10,
                        int(dominantFreqInphase[0][1]) * i + 10,
                    )
                )
            else:
                fftsignal = int(dominantFreqInphase[0][1]) * 2
                var = np.array(
                    range(
                        (fftsignal * i) - int(dominantFreqInphase[0][1]) - 10,
                        (fftsignal * i) - int(dominantFreqInphase[0][1]) + 10,
                    )
                )
            j = i - 2
            dominantfreqvalues[j,0:20] = var 

        for i in range(len(dominantfreqvalues)):    
            tmpMax = max(self.fftValues[dominantfreqvalues[i,:]])
            tmpMaxHz = np.where(tmpMax == self.fftValues)
            Hzval = self.fftTime[tmpMaxHz[0][0]]
            varlist = [tmpMax, tmpMaxHz[0][0], Hzval] 
            j = i + 1
            dominantFreqInphase[j,0:3] = varlist
        self.dominantfreqvalues = dominantfreqvalues
        self.inphase = dominantFreqInphase
        
    def outphase(self,hzMax, hzMin):
        dominantfreqoutphase = np.empty((9,3),float)
        dominantfreqvalues2 = np.empty((9,20), int)
        if (hzMax > 1.5):
            dominantfreqvalues2[1:9,:] = self.dominantfreqvalues - (int(self.inphase[0][1] / 2))
            dominantfreqvalues2[0,:] = dominantfreqvalues2[1,:] - int(self.inphase[0][1])
        else: 
            dominantfreqvalues2[1:9,:] = self.dominantfreqvalues + (int(self.inphase[0][1]))
            dominantfreqvalues2[0,:] = dominantfreqvalues2[1,:] - (int(self.inphase[0][1] * 2))

        for i in range(len(dominantfreqvalues2)):    
            tmpMax = max(self.fftValues[dominantfreqvalues2[i,:]])
            tmpMaxHz = np.where(tmpMax == self.fftValues)
            Hzval = self.fftTime[tmpMaxHz[0][0]]
            varlist = [tmpMax, tmpMaxHz[0][0], Hzval] 
            dominantfreqoutphase[i,0:3] = varlist
        self.outphase = dominantfreqoutphase
        
    def width(self):
        half = self.inphase[0][0] / 2
        num = int(self.inphase[0][1])
        for _ in range(50):
            num += 1
            if (self.fftValues[num] <= half):
                self.first = num
        num = int(self.inphase[0][1])
        for _ in range(50):
            num -= 1
            if (self.fftValues[num] <= half):
                self.second = num
        self.width = self.fftTime[self.first] - self.fftTime[self.second] 
        
    def slope(self):
        slope1 = (self.inphase[0][0] - self.fftValues[self.first])   / (self.first - (int(self.inphase[0][1])))
        slope2 = (self.inphase[0][0] - self.fftValues[self.second])  / ((int(self.inphase[0][1])) - self.second)
        self.slope = np.mean([slope1, slope2])
        
    def density(self):
        SDPrange = range((int(self.inphase[0][1])) -2, (int(self.inphase[0][1])) + 3)
        self.SDP = sum(self.fftValues[SDPrange])
     
    def printje(self):
        if self.direction == 'ML':
            print("stridefreq: ", self.inphase[0][2] )
        else:
            print("stepfreq: ", self.inphase[0][2] )
        print("harmonicratio: ", self.harmonicratio)                                         
        print("harmonic index: ", self.harmonicindex )                                        
        print("Width of the dominant peak (50%)", self.width )
        print("Slope of dominant peak (50%)", self.slope )
        print("Density of dominant peak", self.SDP )
        print("Amplitude of dominant peak", self.dominantpeak )
        print('\n')
        


