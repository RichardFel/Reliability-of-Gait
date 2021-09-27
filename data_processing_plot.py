import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

#sns.set_style("darkgrid")
sns.despine()
sns.set_context("paper",font_scale=1.25)

acceleration = sensors['leftfoot'].acceleration
#pd.DataFrame(acceleration).to_csv('acceleration_example.csv')
acceleration = pd.read_csv('acceleration_example.csv', index_col = 0)
acceleration['Time [s]'] =  np.arange(0,len(acceleration)/100,0.01)
acceleration.rename(columns = {'0': 'Acceleration AP [G]',
                               '1': 'Acceleration ML [G]',
                               '2': 'Acceleration VT [G]'}, inplace = True)

fig1, axICC = plt.subplots(1, figsize = (25,15), dpi = 110)

sns.lineplot(data = acceleration, 
             x = 'Time [s]',
             y = 'Acceleration ML [G]',
             ax = axICC
             ) 
axICC.set_title('Two minute walking of a stroke subject recorded using an ineartiel measurement unit')
axICC.legend(['Left foot sensor'])
plt.savefig('acceleration_ML.png', dpi = 500)

