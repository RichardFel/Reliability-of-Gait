import os

import pandas as pd
import numpy as np

iccValue = 0.75
mainDirectory = os.getcwd()
directory = mainDirectory + '/Results'
os.chdir(directory)
loadfile = 'gait_features_ICC.xlsx'
xls = pd.read_excel(loadfile, index_col = 0)
os.chdir(mainDirectory)

for num, idx in enumerate((xls.transpose())):
    varnum = num + 1
    name = f'{varnum}. {idx}'
    values = xls.loc[idx]
    icc = values.ICC_CI
    mdc = values.MDC_SEM
    mdc_std = round(values.MDC / np.mean([values.test_std,values.hertest_std]),2)
    meanT = values.test_mean_std
    meanH = values.hertestmean_std
    if values.ICC >= 0.75:
        print('&&' + f'{name} ' + '& \ textbf{' + f'{icc}' + '} & ' + f'{mdc} ' + '& ' + f'{mdc_std}' + ' && ' + f'{meanT}' + ' && ' + f'{meanH}' + str(' \ \ '))
    else:
        print(str(f'&& {name}  &  {icc}  &  & &&  {meanT} &&  {meanH}\ \ '))
        
    # Left foot
    if num == 20:
        print('\n')
    elif num == 24:       
        print('\n')
        
    # Right foot
    elif num == 45:       
        print('\n')
    elif num == 66:   
        print('\n')
    elif num == 70:   
        print('\n')    
        
    # Low Back
    elif num == 91:       
        print('\n')
    elif num == 106:   
        print('\n')
    elif num == 124:   
        print('\n')    
        
    # asymm
    elif num == 145:       
        print('\n')