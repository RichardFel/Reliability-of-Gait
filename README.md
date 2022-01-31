This algorithm is devoloped by R. Felius 27/08/2020 in collaboration with Hogeschool Utrecht,
Vrije universiteit Amsterdam, De Parkgraaf en de Hoogstraat Revalidatie.
Modified at 25/06/2021

# Gait analysis
This script is written to analyse data from inertial measurment units-based gait assessment.
This script was created for the project: Making sense of sensor data for personalised healthcare.
The algorithm is used to compute the results for the article: Reliability of IMU-Based Gait Assessment in Clinical Stroke Rehabilitation by R. Felius (2022).
The algorithm was designed to determine gait features in people after stroke with a very slow and poor walking pattern, however can also be used
for elderly and healthy participants.

## How to use the algoritm
Make sure all dependencies are correctly installed.
Place the data from the three IMU files (2 feet, 1 low back) in the data folder.
Run the Main.py file.
The results will appear in an excel in the results folder.
For figures set plotje = True in the Main.py file
For information about the outcomes set verbose = True
For information about files with an error set debug = True

## Testing
Testing files can be found in the Example poor, example average and example good.zip
To run the code place the IMU data  in the Data folder & open the gyroscopeErrorDF.csv.zip and place the CSV file in the Calibration folder.
For the making sense project the IMU data was placed in the DataMakingSense folder.


## Input
The input consists of data from thee inertial measurement units (6-dof) with a triaxial accelerometer and a triaxial gyroscope,
placed at both feet and the lower back.
The inpu files from the IMUs were in .csv format and contained 7 columns: Timestamp [0], IMU accelerometer [1,2,3] and gyroscope [4,5,6].
The IMUs measured at a sampling rate of 104 samples per second.
Participants were instructed to walk for two minutes on a 14 meter walk path taking right turns.
Prior and post measuremetn participants stood still to be able to detect the start and the end of the trial.

## Output
The output consists of 167 gait features, including spatio-temporal, frequency, complexity and asymmetry.
All results are stored in an excel file.

## Functionality
First, the IMU data is loaded and the gyroscope bias is corrected and the signal is down sampled to 100 Hz.
Second, the length of the data is evaluated based on the stationairy periods at the beginning and the end of the signal.
If the signal deviates from the expected signal length the analys stops.
Third, spatio-temporal features for both feet are calculated, including number of steps and distance
Fourth,  frequency features are calculated
Fift,  spatio-temporal features for the low back are calculated
Sixth,  complexity features are calculated
Seventh, asymmetry features are calculated
Lastly, the results are saved in an excel file.

## Resources
Bruijn, S., Bregman, D., Meijer, O., Beek, P., & Van Dieen, J. (2011, 08).
Maximum lyapunov exponents as predictors of global gait stability: A
modelling approach. Medical engineering & physics, 34, 428-36. doi:
10.1016/j.medengphy.2011.07.024

Bugané, F., Benedetti, M. G., Casadio, G., Attala, S., Biagi, F., Manca,
M., & Leardini, A. (2012). Estimation of spatial-temporal gait parameters
in level walking based on a single accelerometer: Validation on normal
subjects by standard gait analysis. Computer Methods and Programs in
Biomedicine, 108(1), 129–137. doi:10.1016/j.cmpb.2012.02.003

Felius, R.A.W.; Geerars, M.; Bruijn, S.M.; van Dieën, J.H.; Wouda, N.C.; Punt, M. Reliability of
IMU-Based Gait Assessment in Clinical Stroke Rehabilitation.
Sensors 2022, 22, 908. https://doi.org/10.3390/s22030908

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



## Help
For questions about the algorithm and the implementations please contact: Richard.felius@hu.nl
