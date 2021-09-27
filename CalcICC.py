import os

import pandas as pd
import numpy as np
import pingouin as pg

mainDirectory = os.getcwd()


def calculateICCMDC():
    filename = 'gait_features'
    directory = mainDirectory + '/Results'
    os.chdir(directory)       
    loadfile = filename + '.xlsx'
    xls = pd.read_excel(loadfile, index_col = 0)
    nFilesPP = 2
    xls.reset_index(inplace = True)
    countValues = xls['Subject number'].value_counts()
    inComplete = countValues.loc[countValues != nFilesPP].index
    xls.drop(xls.loc[xls['Subject number'].isin(inComplete)].index, inplace = True)
    '''
    xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
    # 13,14 = Stapjes: S014P       
    xls.drop(xls.loc[xls['Subject number'] == 'S014P'].index, inplace = True)
    '''        
            
    results = pd.DataFrame(columns = xls.columns[3:]).astype(float)
    results = results.append(pd.Series(name='ICC', dtype = 'float64'))
    results = results.append(pd.Series(name='MDC', dtype = 'float64'))
    
        
    for variable in xls.columns[3:]:
        variableDF = xls[['Subject number', 'Test Type',  variable]]
        icc = pg.intraclass_corr(data=variableDF, targets='Subject number', raters = 'Test Type',
                                 ratings=variable).round(10)
        ICC = icc['ICC'].loc[1]
        CI = icc['CI95%'].loc[1]
        SEM = (np.std(variableDF.loc[:,variable]) * np.sqrt(1 - ICC))
        MDC = (1.96 * SEM * np.sqrt(2))
        SEM = SEM.round(3)
        ICC_CI = str(ICC.round(3))+ ' ['+ str(CI[0]) + ',' + str(CI[1]) + ']'    
        MDC_SEM = str(MDC.round(3))+ ' (' + str(SEM) + ')'
        results.loc['ICC',variable] = ICC
        results.loc['ICC_CI',variable] = ICC_CI
        results.loc['MDC',variable] = MDC
        results.loc['MDC_SEM',variable] = MDC_SEM
        
        test = xls.loc[0::2 , variable]
        meantest = np.mean(test)
        stdtest = np.std(test)
        
        hertest = xls.loc[1::2, variable]
        meanhertest = np.mean(hertest)
        stdhertest = np.std(hertest)
            
        first = str(round(meantest,3)) + ' (' + str(round(stdtest,3)) + ')'
        second = str(round(meanhertest,3)) + ' (' + str(round(stdhertest,3)) + ')'
        
        results.loc['test_mean_std',variable] = first
        results.loc['test_mean',variable] = meantest 
        results.loc['test_std',variable] = stdtest 
        
        results.loc['hertestmean_std',variable] = second
        results.loc['hertestmean',variable] = meanhertest
        results.loc['hertest_std',variable] = stdhertest 
                  

    saveDirectory = mainDirectory + '/Results'
    os.chdir(saveDirectory)
    results = results.transpose()
    save_xls = filename + '_ICC.xlsx'
    results.to_excel(save_xls)
    
    os.chdir(mainDirectory)
     

if __name__ == '__main__':
    calculateICCMDC()
    
    
    
