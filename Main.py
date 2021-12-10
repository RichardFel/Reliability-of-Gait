
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
sys.path.append(str(mainDirectory + '/Calibration'))
sys.path.append(str(mainDirectory + '/Functions'))

from CalcGaitFeatures import calcFeatures


def main():
    calcFeatures(subject = 'S001', testType = 'Test', plotje=True, verbose=True, debug = True)

if __name__ == '__main__':
    main()


'''
Literature:  
    Bruijn, S., Bregman, D., Meijer, O., Beek, P., & Van Dieen, J. (2011, 08).
Maximum lyapunov exponents as predictors of global gait stability: A
modelling approach. Medical engineering & physics, 34, 428-36. doi:
10.1016/j.medengphy.2011.07.024

    Bugané, F., Benedetti, M. G., Casadio, G., Attala, S., Biagi, F., Manca, 
M., & Leardini, A. (2012). Estimation of spatial-temporal gait parameters 
in level walking based on a single accelerometer: Validation on normal 
subjects by standard gait analysis. Computer Methods and Programs in 
Biomedicine, 108(1), 129–137. doi:10.1016/j.cmpb.2012.02.003 

    Helbostad, J., Askim, T., & Moe-Nilssen, R. (2004, 01). Short-term repeatability
of body sway during quiet standing in people with hemiparesis and in frail
older adults 1 1 no commercial party having a direct financial interest in
the results of the research supporting this article has or will confer a benefit
on the author(s) or on any organization with which the author(s) is/are
associated. Archives of Physical  
    
    Ghislieri, M., Gastaldi, L., Pastorelli, S., Tadano, S., & Agostini, V. (2019, 09).
Wearable inertial sensors to assess standing balance: A systematic review.
Sensors, 19, 4075. doi: 10.3390/s19194075

    Mancini, M., Salarian, A., Carlson-Kuhta, P., Zampieri, C., King, L., Chiari, L.,
& Horak, F. (2012, 08). Isway: A sensitive, valid and reliable measure of
postural control. Journal of neuroengineering and rehabilitation, 9, 59. doi:
10.1186/1743-0003-9-59
    
    Pham MH, Elshehabi M, Haertner L, Del Din S, Srulijes K, Heger T, Synofzik M, 
Hobert MA, Faber GS, Hansen C, Salkovic D, Ferreira JJ, Berg D, Sanchez-Ferro Á, 
van Dieën JH, Becker C, Rochester L, Schmidt G and Maetzler W (2017) Validation of a 
Step Detection Algorithm during Straight Walking and Turning in Patients with 
Parkinson’s Disease and Older Adults Using an Inertial Measurement
Unit at the Lower Back. Front. Neurol. 8:457. doi: 10.3389/fneur.2017.00457
'''
