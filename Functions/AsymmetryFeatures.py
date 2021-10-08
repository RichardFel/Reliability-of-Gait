import numpy as np

def calcFeatures(sensors):
    asymmetryResults = Asymmetry(sensors)
    asymmetryResults.asymmetryFeet()
    asymmetryResults.asymmetryLowback(sensors['lowback'])
    asymmetryResults.normalised(sensors)
    return asymmetryResults
        
class Asymmetry:
    def __init__(self, sensors):
        try:   
            parFoot = sensors['leftfoot'].parFoot
        except:
            parFoot = 'left'
        if parFoot != 'R':
            self.parFoot     = sensors['leftfoot']
            self.NonParFoot  = sensors['rightfoot']
        else:
            self.parFoot     = sensors['rightfoot']
            self.NonParFoot  = sensors['leftfoot']  

    def meanPar_NonPar(self, par, nonpar, begin, end):
        outpar = np.array([])
        outnonpar = np.array([])
        
        for i in par[begin:-end]:
            outpar = np.concatenate((outpar, np.array([len(i)])))
    
        for i in nonpar[begin:-end]:
            outnonpar = np.concatenate((outnonpar, np.array([len(i)])))
        
        return outpar, outnonpar
    
    def symmetryIndex(self, par, nonpar):
        return ((par / nonpar ) / (0.5 * (par + nonpar)))

    def GaitAsymmetry(self, par, nonpar):
        return 100 * (np.log(par/ nonpar))
    
    def SymmetryAngle(self, par, nonpar):
        return (45 - np.arctan(par/nonpar)) / 90

    def meanParetic(self, arg0, arg1):
        meanPar = np.mean(arg0) * self.parFoot.sampleFreq
        meanNONPar = np.mean(arg1) * self.parFoot.sampleFreq
        return meanPar , meanNONPar     

    def asymmetryFeet(self):
        standPar, standNONPar = self.meanPar_NonPar(self.parFoot.standphases, self.NonParFoot.standphases, 5, 5)
        meanstandPar , meanstandNONPar = self.meanParetic(standPar, standNONPar)
        self.SRstandphase = meanstandPar / meanstandNONPar     
        swingPar, swingNONPar = self.meanPar_NonPar(self.parFoot.swingphases, self.NonParFoot.swingphases, 5, 5)
        meanswingPar , meanswingNONPar = self.meanParetic(swingPar, swingNONPar)
        self.SRswingphase =meanswingPar / meanswingNONPar

        shortest =    np.argmin([len(swingPar),len(swingNONPar),len(standPar),len(standNONPar)])
        if shortest == 0:
            inputlenth = len(swingPar) -1 
        elif shortest == 1:
            inputlenth = len(swingNONPar)-1
        elif shortest == 2:
            inputlenth = len(standPar)-1
        else:
            inputlenth = len(standNONPar)   -1
        swing_stancePar = swingPar[inputlenth] / standPar[inputlenth]
        swing_stanceNONPar = swingNONPar[inputlenth] / standNONPar[inputlenth]
        meanswing_stancePar , meanswing_stanceNONPar = self.meanParetic(swing_stancePar, swing_stanceNONPar)
        self.SRswing_stance = meanswing_stancePar / meanswing_stanceNONPar

        self.SIswing_stancePar = self.symmetryIndex(meanswing_stancePar, meanswing_stanceNONPar)                  
        self.SIstandphase = self.symmetryIndex(meanstandPar, meanstandNONPar)                  
        self.SIswingphase = self.symmetryIndex(meanswingPar,meanswingNONPar)                 
                
        self.GAswing_stancePar = self.GaitAsymmetry(meanswing_stancePar, meanswing_stanceNONPar)                  
        self.GAstandphase = self.GaitAsymmetry(meanstandPar, meanstandNONPar)                  
        self.GAswingphase = self.GaitAsymmetry(meanswingPar,meanswingNONPar)                 
    
        self.SAswing_stancePar = self.SymmetryAngle(meanswing_stancePar, meanswing_stanceNONPar)                  
        self.SAstandphase = self.SymmetryAngle(meanstandPar, meanstandNONPar)                  
        self.SAswingphase = self.SymmetryAngle(meanswingPar,meanswingNONPar)                 
            
        accelerationPar = self.parFoot.acceleration[:, 2]
        accelerationNonPar = self.NonParFoot.acceleration[:, 2]
        peaksPar = accelerationPar[self.parFoot.peaks]
        peaksNonPar = accelerationNonPar[self.NonParFoot.peaks]

        if len(peaksPar ) > len(peaksNonPar):
            peakDiff = (peaksPar[0:len(peaksNonPar)] -peaksNonPar)
        elif len(peaksNonPar ) > len(peaksPar):
            peakDiff = (peaksPar -peaksNonPar[0:len(peaksPar)])
        else:
            peakDiff = (peaksPar -peaksNonPar)
        self.Amplitudeasym = np.mean(peakDiff)
        self.AmplitudeSTDasym = np.std(peakDiff)
    
    
    def asymmetryLowback(self, lowback):
        acceleration = lowback.acceleration[lowback.walkPart,0]
        if lowback.firstStepDir == 'Right':
            lowBackLeft = lowback.peaks[1::2]
            lowBackRight = lowback.peaks[0::2]
        else:
            lowBackLeft = lowback.peaks[0::2]
            lowBackRight = lowback.peaks[1::2]
        peakslowBackLeft= acceleration[lowBackLeft]
        peakslowBackRight = acceleration[lowBackRight]
        if self.parFoot == 'R':
            parFoot     = peakslowBackRight
            NonParFoot  = peakslowBackLeft   
        else:
            parFoot     = peakslowBackLeft
            NonParFoot  = peakslowBackRight
            
        if len(parFoot ) > len(NonParFoot):
            peakDiff = (parFoot[0:len(NonParFoot)  ] -NonParFoot)
        elif len(NonParFoot ) > len(parFoot):
            peakDiff = (parFoot -NonParFoot[0:len(parFoot)  ])
        else:
            peakDiff = (parFoot -NonParFoot)
        self.stepPeakDiffSTD = np.std(peakDiff)
        self.lowBackPeakDiffValues = (np.mean(peakslowBackLeft) / np.mean(peakslowBackRight))

    def normalised(self, sensors) :
        try:
            bh = int(sensors['leftfoot'].bodyHeight)
        except AttributeError:
            bh = 180
        meantotdist = np.mean([sensors['leftfoot'].totdist, sensors['rightfoot'].totdist])
        self.normDistance = meantotdist/bh
        self.normCadence = np.mean([sensors['leftfoot'].cadence, sensors['rightfoot'].cadence]) / bh
        self.normDistancePStride = np.mean([sensors['leftfoot'].meanStrideDistperstep,  sensors['rightfoot'].meanStrideDistperstep])
        TBH = np.sqrt(bh / 9.81)
        self.normTimePerStep = sensors['lowback'].stridetimemean / TBH 
        
    def printje(self):
        print('SRstandphase ', self.SRstandphase)
        print('SRswingphase',self.SRswingphase)
        print('SRswing_stance',self.SRswing_stance) 
        print('SIstandphase  '  , self.SIstandphase)             
        print('SIswingphase   '   ,self.SIswingphase) 
        print('SIswing_stancePar   '   ,self.SIswing_stancePar) 
        print('GAstandphase     ',self.GAstandphase)            
        print('GAswingphase  ', self.GAswingphase)
        print('GAswing_stancePar  ', self.GAswing_stancePar) 
        print('SAstandphase    '  ,self.SAstandphase)           
        print('SAswingphase     '   , self.SAswingphase)  
        print('SAswing_stancePar     '   , self.SAswing_stancePar)  
        print('stepPeakDiffSTD' , self.stepPeakDiffSTD )
        print('lowBackPeakDiffValues',  self.lowBackPeakDiffValues)
        print('Amplitudeasym', self.Amplitudeasym)
        print('AmplitudeSTDasym',self.AmplitudeSTDasym)
            

