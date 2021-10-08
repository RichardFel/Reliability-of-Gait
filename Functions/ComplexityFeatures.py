import statsmodels.tsa.api as smt
import numpy as np
import Visualise
import Proces

def calcFeatures(sensors, plotje, verbose):
    autocovariance(sensors['leftfoot'], plotje = plotje)
    autocorrelation(sensors['leftfoot'], plotje = plotje)
    autocovariance(sensors['rightfoot'],plotje = plotje)
    autocorrelation(sensors['rightfoot'], plotje = plotje)
    autocovariance(sensors['lowback'], plotje = plotje)
    autocorrelation(sensors['lowback'], plotje = plotje)  

    lyapunov(sensors['lowback'],NumbOfSteps = 50,new_sf = 50,firststride = 8,ndim = 5, delay = 15, nnbs = 5, plotje = plotje)
    lyapunov(sensors['leftfoot'],NumbOfSteps = 25,new_sf = 100,firststride = 4,ndim = 5, delay = 15, nnbs = 5, plotje= plotje)
    lyapunov(sensors['rightfoot'],NumbOfSteps = 25,new_sf = 100,firststride = 4,ndim = 5, delay = 15, nnbs = 5, plotje= plotje)
    
    entropy(sensors['lowback'], NumbOfSteps = 15, firststride = 10, m = 2, r = 0.25)    
    entropy(sensors['leftfoot'], NumbOfSteps = 25,firststride = 5,m = 2, r = 0.25)  
    entropy(sensors['rightfoot'], NumbOfSteps = 25,firststride = 5,m = 2, r = 0.25)  
    return sensors

def autocovariance(self, plotje = None):
    lag = int(self.dominantFreq * 3)
    self.autocovx_acc_ser = smt.acovf(self.acceleration[self.walkPart,0], demean = True, nlag = lag, fft = True)
    self.autocovx_acc = np.max(self.autocovx_acc_ser[10:])
    self.autocovy_acc_ser = smt.acovf(self.acceleration[self.walkPart,1], demean = True,  nlag = lag, fft = True)
    self.autocovy_acc = np.max(self.autocovy_acc_ser[10:])
    self.autocovz_acc_ser = smt.acovf(self.acceleration[self.walkPart,2], demean = True, nlag = lag, fft = True)
    self.autocovz_acc = np.max(self.autocovz_acc_ser[10:])
    self.autocovx_gyr_ser = smt.acovf(self.gyroscope[self.walkPart,0], demean = True,  nlag = lag, fft = True)
    self.autocovx_gyr = np.max(self.autocovx_gyr_ser[10:])
    self.autocovy_gyr_ser = smt.acovf(self.gyroscope[self.walkPart,1],  demean = True,  nlag = lag, fft = True)
    self.autocovy_gyr = np.max(self.autocovy_gyr_ser[10:])
    self.autocovz_gyr_ser = smt.acovf(self.gyroscope[self.walkPart,2], demean = True,  nlag = lag, fft = True)
    self.autocovz_gyr = np.max(self.autocovz_gyr_ser[10:])
   
    if plotje:
        array = np.transpose(np.array([self.autocovx_acc_ser, self.autocovy_acc_ser,self.autocovz_acc_ser]))
        Visualise.plot4(array,'Autocovariance acceleration', 'Samples', 'Overlap')
        array = np.transpose(np.array([self.autocovx_gyr_ser, self.autocovy_gyr_ser,self.autocovz_gyr_ser]))
        Visualise.plot4(array,'Autocovariance gyroscope', 'Samples', 'Overlap')

def autocorrelation(self,  plotje = None):
    lag = int(self.dominantFreq * 3)
    self.autocorx_acc_ser = smt.acf(self.acceleration[self.walkPart,0], nlags = lag, fft = True)
    self.autocorx_acc = np.max(self.autocovx_acc_ser[10:])
    self.autocory_acc_ser = smt.acf(self.acceleration[self.walkPart,1], nlags = lag, fft = True)
    self.autocory_acc = np.max(self.autocovy_acc_ser[10:])
    self.autocorz_acc_ser = smt.acf(self.acceleration[self.walkPart,2], nlags = lag, fft = True)
    self.autocorz_acc = np.max(self.autocovz_acc_ser[10:])
    self.autocorx_gyr_ser = smt.acf(self.gyroscope[self.walkPart,0], nlags = lag, fft = True)
    self.autocorx_gyr = np.max(self.autocovx_gyr_ser[10:])
    self.autocory_gyr_ser = smt.acf(self.gyroscope[self.walkPart,1], nlags = lag, fft = True)
    self.autocory_gyr = np.max(self.autocovy_gyr_ser[10:])
    self.autocorz_gyr_ser = smt.acf(self.gyroscope[self.walkPart,2], nlags = lag, fft = True)
    self.autocorz_gyr = np.max(self.autocovz_gyr_ser[10:])
        
def lyapunov(self,NumbOfSteps,new_sf,firststride,ndim, delay, nnbs, plotje):
    Proces.resample(self,  NumbOfSteps, firststride, new_sf, input_signal = self.acceleration)   
    statespace(self, ndim = ndim, delay = delay)    
    rosenstein(self, new_sf, period = 1, ws = 0.5, nnbs = nnbs, plotje = plotje)
    
def statespace(self, ndim = 5, delay = 10):
    signal = self.resampled
    try:
        m,n = signal.shape
        self.state = np.zeros((m - delay * (ndim ), ndim,n))
    except ValueError:
        m = len(signal)
        self.state = np.zeros((m - delay * (ndim ), ndim,1))

    for i_dim in range(ndim):          
        self.state[:,i_dim,:] = signal[i_dim*delay:len(signal)-(ndim - i_dim) * delay]

def rosenstein(self, new_sf, period = 1, ws = 0.5, nnbs = 5, plotje = None):
    m,n,o = self.state.shape
    ws = int(ws * new_sf)
    emptyarray = np.empty((ws,n,o))
    emptyarray[:] = np.nan
    state = np.concatenate((self.state, emptyarray),axis = 0)
    divergence = np.zeros((m*nnbs,ws,o))
    difference = np.zeros((m+ws,n,o))
    self.lde = np.zeros(o)
    for _, column in enumerate(range(o)):
        counter = 0
        for sample in range(m): 
            for neighbour in range(n): 
                difference[:,neighbour,column] = np.subtract(state[:,neighbour,column],state[sample,neighbour,column]) ** 2
                
            start_index = int(np.max([0,sample-int(0.5*new_sf*period)]))   
            stop_index = int(np.min([m,sample+int(0.5*new_sf*period)]))   
            difference[start_index:stop_index,:,column] = np.nan        
            index = np.sum(difference[:,:,column],axis = 1).argsort()
            
            for neighbour in range(0,nnbs):
                div_tmp = np.subtract(state[sample:sample+ws,:,column],state[index[neighbour]:index[neighbour]+ws,:,column])
                divergence[counter,:,column] =  np.sqrt(np.sum(div_tmp**2,axis = 1)) 
                counter += 1 
                
        divmat =np.nanmean(np.log(divergence[:,:,column]),0);   
        xdiv =  np.linspace(1,len(divmat), num = int(0.5*new_sf*period))
        Ps = np.polynomial.polynomial.polyfit(xdiv, divmat[0:int(np.floor(0.5 * period * new_sf))],1)
            
        sfit = np.polynomial.Polynomial(Ps)
        self.lde[column] = Ps[1]

        if plotje:
            Visualise.plot3(divmat, sfit(xdiv),title = 'Lyapunov Rosenstein' ,
                                 xlabel = 'time [s]', ylabel = 'divergence',
                                 legend1 = 'divergence', legend2 = 'lde short'
                                 )
            
def entropy(self, NumbOfSteps, firststride, m, r):            
    select = self.acceleration[self.peaks[firststride]:self.peaks[NumbOfSteps+firststride]]
    self.approxentropy_accX = aproximateEntropy(m, r = (r * np.std(select[:,0] )), signal = select[:,0])
    self.approxentropy_accY = aproximateEntropy(m, r = (r * np.std(select[:,1] )), signal = select[:,1])
    self.approxentropy_accZ = aproximateEntropy(m, r = (r * np.std(select[:,2] )), signal = select[:,2])
    self.sampleEntropy_accX = sampleEntropy(m, r = (r * np.std(select[:,0] )), signal = select[:,0])
    self.sampleEntropy_accY = sampleEntropy(m, r = (r * np.std(select[:,1] )), signal = select[:,1])
    self.sampleEntropy_accZ = sampleEntropy(m, r = (r * np.std(select[:,2] )), signal = select[:,2])

def count_vectors(m, r, N, signal):
    C = np.zeros((len(signal)-m +1,1))
    for i in range(N-(m-1)):
        tmpSignal = signal[i:]
        checkValues = tmpSignal
        for j in range(m):
            refValue = signal[i+j]
            minVal = refValue - r
            maxVal = refValue + r
            matchesIDX = np.where((checkValues >= minVal) & (checkValues <= maxVal))[0]
            if j == 0:
                initmatchesIDX = matchesIDX
                folNumbIDX = matchesIDX + 1
            else:
                initmatchesIDX = initmatchesIDX[matchesIDX]
                folNumbIDX = initmatchesIDX + 1 + j
            try:
                checkValues = tmpSignal[folNumbIDX]
            except IndexError: 
                checkValues = tmpSignal[folNumbIDX[:-1]]
                
        C[i] += len(matchesIDX)    
        
        try:
            C[(folNumbIDX[1:]-1 - j + i)] += 1
        except:
            continue
        
    return C

def aproximateEntropy(m, r, signal):
    m_2 = m + 1
    N = len(signal)
    firstResult = count_vectors(m, r, N, signal)
    logFR = np.sum(np.log(firstResult/ (N - m + 1)))
    phi = logFR / (N - m + 1)
    secondResult = count_vectors(m_2, r, N, signal)
    logSR = np.sum(np.log(secondResult / (N - m)))
    phi_2 = logSR / (N - m)
    return phi - phi_2


def sampleEntropy(m, r, signal):
    m_2 = m + 1
    N = len(signal)
    firstResult = count_vectors(m, r, N, signal) - 1 
    logFR = np.sum((firstResult / (N - m))) / (N- m)
    phi = logFR * (( (N-m - 1)* (N-m)) / 2)
    secondResult = count_vectors(m_2, r, N, signal) - 1
    logSR = np.sum(secondResult / (N - m_2))  / (N- m)
    phi_2 = logSR * (( (N-m - 1)* (N-m)) / 2)
    return -np.log( phi_2 /phi)
        

