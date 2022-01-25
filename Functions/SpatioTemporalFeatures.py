import numpy as np
import Visualise
import SensorFusion
import StepDetection

def calcFeaturesFeet(sensors, plotje, verbose, per_N_strides):
    sensors = StepDetection.detectStepsFeet(sensors,plotje, verbose)       
    stepTime(sensors["leftfoot"], per_N_strides,verbose, 'leftfoot')
    stepTime(sensors["rightfoot"], per_N_strides,verbose, 'rightfoot')
    SensorFusion.rotateToGlobal(sensors["leftfoot"], sensors["rightfoot"],plotje)
    descriptives(sensors["leftfoot"],  per_N_strides)
    descriptives(sensors["rightfoot"],  per_N_strides)
    stepDistance(sensors["leftfoot"], per_N_strides,plotje,verbose, 'leftfoot' )
    stepDistance(sensors["rightfoot"], per_N_strides, plotje, verbose, 'rightfoot')   
    if (np.abs(sensors["leftfoot"].totdist -sensors["rightfoot"].totdist) > 25):
        print('Difference between distance too large. We cannot include',
              'this participant')
        raise Exception 
    if verbose:
        print('\n checkpoint 3 passed \n')
    return sensors

def stepTime(self, per_N_strides, verbose, foot):
    timepersteride = []
    stridetimemean = []
    stridetimeSTD = []
    normstridetime = []
    for i in range(int(np.floor(len(self.peaks[5:-5]) / per_N_strides))):
        tmpVal = np.diff(self.peaks[per_N_strides*i+5:per_N_strides*i+6+per_N_strides])*self.sampleFreq
        timepersteride.append(tmpVal)
        stridetimemean.append(np.mean(tmpVal))
        stridetimeSTD.append(np.std(tmpVal))
        normstridetime.append( np.std(tmpVal) / tmpVal)
    self.timepersteride = timepersteride
    self.stridetimemean = np.mean(stridetimemean)
    self.stridetimeSTD = np.mean(stridetimeSTD)
    self.normstridetime = np.mean(normstridetime)  
    self.cadence = int(len(self.peaks)/2)
    if verbose:
        print(foot)
        print("Amount of stride in trial: ", self.stridenum)
        print("Mean time per stride: ", self.stridetimemean, 's')
        print("Step time STD: ", self.stridetimeSTD)
        print("Normalised step time: ",  self.normstridetime )
        print("\n")
        
def stepDistance(self, per_N_strides, plotje = None, verbose = None, foot = None):
    forwardvelocity = np.hypot(np.abs(np.diff(self.velocity[:,0])),np.abs(np.diff(self.velocity[:,1])))
    forwarddisplacement = np.hypot(np.cumsum(np.abs(np.diff(self.position[:,0]))),np.cumsum(np.abs(np.diff(self.position[:,1]))))
    strideDist = np.zeros(self.stridenum)
    strideVel = np.zeros(self.stridenum)
    
    for count, value in enumerate(self.standphases[:-1]):
        strideDist[count] = np.abs(np.diff((forwarddisplacement[value[-1]],forwarddisplacement[self.standphases[count+1][0]])))[0]
        try:
            strideVel[count] = np.max(self.velocity[value[-1]:self.standphases[count+1][0]])
        except ValueError:
            strideVel[count] = 0
    strideDist = strideDist[np.where(strideDist < 2* np.mean(strideDist))[0]]
    strideVel = strideVel[np.where(strideDist < 2* np.mean(strideDist))[0]]
    displacement  = np.sum(strideDist)
    meanStrideDistperstep = []
    stdStrideDistperstep= []
    meanstrideVelperstepperstep= []
    stdstrideVelperstepperstep= []
    for i in range(int(np.floor(len(strideDist[5:-5]) / per_N_strides))):
        tmpValPos = strideDist[per_N_strides*i+5:per_N_strides*i+5 + per_N_strides]
        meanStrideDistperstep.append(np.nanmean(tmpValPos))
        stdStrideDistperstep.append(np.std(tmpValPos))
        tmpValVel = strideVel[per_N_strides*i+5:per_N_strides*i+5 + per_N_strides]
        meanstrideVelperstepperstep.append(np.nanmean(tmpValVel))
        stdstrideVelperstepperstep.append(np.std(tmpValVel))
    self.kmph = (np.max(displacement ) * 30) / 1000
    self.totdist = np.max(displacement )
    self.meanStrideDistperstep = np.nanmean(meanStrideDistperstep)
    self.stdStrideDistperstep = np.nanmean(stdStrideDistperstep)
    self.meanstrideVelperstepperstep = np.nanmean(meanstrideVelperstepperstep)
    self.stdstrideVelperstepperstep  = np.nanmean(stdstrideVelperstepperstep)

    if verbose:
        printje(self, forwarddisplacement, foot)

    if plotje:
        Visualise.plot2(forwardvelocity, forwarddisplacement,
                             title = 'Forward velocity and position',
                             xlabel = 'Time in seconds', ylabel1 = 'Velocity [m/s]',
                             ylabel2 = 'Position [m]'
                             )

def printje(self, forwarddisplacement, foot):
    print(foot)
    print('Distance walked: ',  np.max(forwarddisplacement ), 'm')
    print('Mean distance per stride: ',  self.meanStrideDistperstep)
    print('STD distance per stride: ',  self.stdStrideDistperstep)
    print('Mean velocity per stride: ',  self.meanstrideVelperstepperstep )
    print('STD velocity per stride: ',  self.stdstrideVelperstepperstep )
    print('Kilometer per hour: ',  self.kmph)

def descriptives(self, per_N):
    accrangeAP = []
    accrmsAP= []
    accrangeML= []
    accrmsML= []
    accrangeVT= []
    accrmsVT= []
    gyrrangeAP = []
    gyrrmsAP= []
    gyrrangeML= []
    gyrrmsML= []
    gyrrangeVT= []
    gyrrmsVT= []
    for i in range(int(np.floor(len(self.peaks[5:-5])/per_N))):
        selectACC = self.accRotated[self.peaks[5+per_N*i]:self.peaks[5+per_N+per_N*i]]  
        accrangeAP.append(np.max(selectACC[:,0]) - np.min(selectACC[:,0]))
        accrmsAP.append(np.sqrt(np.mean(selectACC[:,0]**2)))
        accrangeML.append(np.max(selectACC[:,1]) - np.min(selectACC[:,1]))
        accrmsML.append(np.sqrt(np.mean(selectACC[:,1]**2)))
        accrangeVT.append(np.max(selectACC[:,2]) - np.min(selectACC[:,2]))
        accrmsVT.append(np.sqrt(np.mean(selectACC[:,2]**2)))
        selectGYR = self.gyrRotated[self.peaks[5+per_N*i]:self.peaks[5+per_N+per_N*i]]  
        gyrrangeAP.append(np.max(selectGYR[:,0]) - np.min(selectGYR[:,0]))
        gyrrmsAP.append(np.sqrt(np.mean(selectGYR[:,0]**2)))
        gyrrangeML.append(np.max(selectGYR[:,1]) - np.min(selectGYR[:,1]))
        gyrrmsML.append(np.sqrt(np.mean(selectGYR[:,1]**2)))
        gyrrangeVT.append(np.max(selectGYR[:,2]) - np.min(selectGYR[:,2]))
        gyrrmsVT.append(np.sqrt(np.mean(selectGYR[:,2]**2)))
    self.accrangeAP = np.mean(accrangeAP)                              
    self.accrmsAP = np.mean( accrmsAP)
    self.accrangeML = np.mean(accrangeML)                 
    self.accrmsML = np.mean(accrmsML)  
    self.accrangeVT = np.mean(accrangeVT)                         
    self.accrmsVT = np.mean(accrmsVT)  
    self.gyrrangeAP = np.mean(gyrrangeAP)                              
    self.gyrrmsAP =  np.mean(gyrrmsAP)
    self.gyrrangeML = np.mean(gyrrangeML)                 
    self.gyrrmsML = np.mean(gyrrmsML)  
    self.gyrrangeVT = np.mean(gyrrangeVT)                         
    self.gyrrmsVT = np.mean(gyrrmsVT)  

def calcFeaturesLowback(sensors, plotje, verbose, per_N_steps):
    StepDetection.stepdetectionLowback(sensors, per_N_steps, plotje, printje)
    descriptives(sensors['lowback'], per_N_steps)
    stepTime(sensors['lowback'], per_N_steps, verbose, 'lowback')
    if (np.abs(len(sensors['lowback'].peaks) - (sensors['leftfoot'].stridenum + sensors['rightfoot'].stridenum)) > 20):
        print('We cannot find the same amount of peaks in LB as in feet sensors.','Participant cannot be included')
        raise Exception 
    if verbose:
        print('\n', 'checkpoint 4 passed','\n')
    return sensors
