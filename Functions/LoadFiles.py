import pandas as pd
import numpy as np
import os
import Visualise

class loadCsv:  
    def __init__(self, owd,fileName, plotje,resample,makingSense,locInExcel,subject,testType,):
        '''
        This function is used to create an object of the sensor data that 
        contains the sample frequency, raw acceleration [m/s^2] and corrected 
        gyroscope ('rad/s'). This object will be further used in functions to 
        store variables. 
        The first 200 and last 200 samples are always skipped.
        The gyroscope is converted to rad/s.
        The gyroscope constant bias error is corrected using values determined in a 
        static test. To add a new calibration file go to: main_files/add_calibration
        Samplefrequenty is calculated based on the IMU timestamps
        Possibility to plot the raw acceleration adn gyroscope signal.
        '''
        self.loadLog(owd, fileName, makingSense,locInExcel,subject,testType)
        self.dataToFloat()
        self.resampleData(resample)
        self.correctGyroscope(owd)
        if plotje:
            self.plotRawData()

    def loadLog(self, owd, fileName, makingSense,locInExcel,subject,testType,):
        if makingSense:
            fileName = self.loadMakingSense(fileName, owd,subject,locInExcel,testType)
        else:
            os.chdir((owd + '/Data'))
        self.serialnumber = pd.read_csv(fileName, nrows=1).loc[0][0]  # Get sensor serial number to correct gyroscope bias
        self.data = pd.read_csv(fileName,                                           # Load the log file
                                header = 0,                       
                                names = ['T', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'], 
                                skiprows = 9, 
                                sep = ',',
                                error_bad_lines = False
                                )  
                                
    def loadMakingSense(self,fileName, owd,subject,locInExcel,testType):
        subject_dir = '/DataMakingSense/' + subject
        os.chdir((owd + subject_dir))
        normData = pd.read_excel('Excel_logbestanden' + subject + '.xlsx',nrows=0)  
        self.parFoot = normData.columns[5]
        self.bodyHeight = normData.columns[3]
        xls = pd.read_excel('Excel_logbestanden' + subject + '.xlsx',skiprows=4)  
        if fileName == 'leftfoot.csv':        

            os.chdir(owd + subject_dir + '/' + testType + '/Linkervoet')
            num = xls.loc[locInExcel, 'Log LV']
        elif fileName == 'rightfoot.csv':
            os.chdir(owd +  subject_dir + '/' + testType + '/Rechtervoet')
            num = xls.loc[locInExcel, 'Log RV']
        else:
            os.chdir(owd + subject_dir + '/' + testType + '/Onderrug')
            num = xls.loc[locInExcel, 'Log OR']

        if isinstance(num, str):  # In case someone wrote logxx instead of only a number
            num = int(num[-2] + num[-1]) if len(num) > 5 else int(num[-1])

        return 'log' + str(num).zfill(3) + '.csv'

    def dataToFloat(self):
        self.data.dropna(how='any', inplace=True)
        for i in self.data.columns[1:]:
            self.data[i] = pd.to_numeric(self.data[i], downcast='float')
            
    def resampleData(self,resample):
        if resample:
            self.resample()
        else:
            self.sampleFreq = 1 / (10000 / np.mean(np.diff(self.data.iloc[:,0])))
            self.acceleration = np.array(self.data.iloc[:, 1:4])
            self.gyroscope = np.radians(np.array(self.data.iloc[:, 4:7]))

    def resample(self):
        tmpsampleFreq = 1 / (10000 / np.mean(np.diff(self.data.iloc[:,0])))
        tmptime = np.array(self.data['T'])
        tmptime = (tmptime - tmptime[0]) / 10000
        newTime = np.arange(0, round(len(tmptime) * tmpsampleFreq,
                            2), 0.01)
        lindx = []
        for i in newTime:
            idx = np.abs(i - tmptime).argmin()
            lindx.append(idx)
        self.gyroscope = np.radians(np.array(self.data.iloc[lindx, 4:7]))
        self.acceleration = np.array(self.data.iloc[lindx, 1:4])
        self.sampleFreq = 0.01

    def correctGyroscope(self, owd):
        try:
            gyorscopeErrorDF = pd.read_csv(owd + '/Calibration/gyorscopeErrorDF.csv', index_col=0)
            (gyrEx, gyrEy, gyrEz) = gyorscopeErrorDF.loc[self.serialnumber]
            self.gyroscope -= (gyrEx, gyrEy, gyrEz)
        except KeyError:
            print (f'Warning: Calibrate this sensor: {self.serialnumber} before using!')

        self.gyroscope = self.gyroscope[200:-200]
        self.acceleration = self.acceleration[200:-200]

    def plotRawData(self):
        Visualise.plot1(self.acceleration,
                                title='Raw acceleration signal',
                                xlabel='Samples',
                                ylabel='Acceleration [g]')
        Visualise.plot1(self.gyroscope,
                                title='Raw gyroscope signal',
                                xlabel='Samples',
                                ylabel='Gyroscope [deg/s]')