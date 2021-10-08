import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

owd = os.getcwd()
os.chdir((owd + '/Data'))
fileName = 'leftfoot.csv'
data = pd.read_csv(fileName, header = 0,                       
                                names = ['T', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'], 
                                skiprows = 9, 
                                sep = ',',
                                error_bad_lines = False
                                )  

def magnitude(signal):                                                         
    return np.sqrt(np.sum(signal * signal, axis = 1))

acceleration = magnitude(data.iloc[:,1:4])
normACC = (acceleration-min(acceleration))/(max(acceleration)-min(acceleration))

gyroscope = magnitude(data.iloc[:,4:7])
normGYR = (gyroscope-min(gyroscope))/(max(gyroscope)-min(gyroscope))

magDF = pd.DataFrame({'Acceleration Magnitude [G]':normACC, 'GYR Magnitude':normGYR})
magDF['Time [s]'] =  np.arange(0,len(magDF)/100,0.01)

fig1, axICC = plt.subplots(1, figsize = (25,15), dpi = 110)
sns.lineplot(data = magDF, 
             x = 'Time [s]',
             y = 'Acceleration Magnitude [G]',
             ax = axICC
             ) 
sns.lineplot(data = magDF, 
             x = 'Time [s]',
             y = 'GYR Magnitude',
             ax = axICC
             ) 
axICC.set_ylabel('Magnitude')
axICC.set_title('Two minute walking of a stroke subject recorded using an inertial measurement unit [left foot]')
axICC.legend(['Acceleration magnitude','Gyroscope magnitude'])
plt.savefig('Magnitude.png', dpi = 500)

