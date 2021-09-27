import os

import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib import ticker


iccValue = 0.75
mainDirectory = os.getcwd()
saveTo = mainDirectory + '/Figures'

#def plotSIT():
directory = mainDirectory + '/Results'
os.chdir(directory)
loadfile = 'gait_features_ICC.xlsx'
xls = pd.read_excel(loadfile, index_col = 0)
os.chdir(mainDirectory)

sns.set_style("darkgrid")
sns.despine()
sns.set_context("paper",font_scale=1.25)


fig1, axICC = plt.subplots(2,2,figsize=(25,25),dpi = 110, gridspec_kw={'width_ratios': [(21/39), (18/39)]})
plt.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.20, right=None, top=0.95, wspace=0.02, hspace=0.05)



icc = xls.ICC 
xaxis = range(1,len(icc)+1)
target = np.ones(len(xls)) * iccValue

mdc = np.ones(len(xls)) * 1000
for i in range(len(xls)):
    if xls.ICC[i] > iccValue:
        mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))

data_plot = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
data_plot['Type']  = 0
data_plot['Sensor']  = 0

# Left foot
data_plot.loc['Stride time mean L':'SampEN VT L','Sensor'] = 'leftfoot'
data_plot.loc['Stride time mean L':'RMS gyr VT L','Type'] = 'Spatio-Temporal' 
data_plot.loc['Stride time mean L':'RMS gyr VT L','xaxis'] = np.arange(1,22)

data_plot.loc['Dominant peak freq L':'Dominant peak density L','Type'] = 'Frequency' 
data_plot.loc['Dominant peak freq L':'Dominant peak density L','xaxis'] = np.arange(22,26)

data_plot.loc['ACOV acc AP L':'SampEN VT L','Type'] = 'Complexity' 
data_plot.loc['ACOV acc AP L':'SampEN VT L','xaxis'] = range(40,61)

# right foot
data_plot.loc['Stride time mean R':'SampEN VT R','Sensor'] = 'rightfoot'
data_plot.loc['Stride time mean R':'RMS gyr VT R','Type'] = 'Spatio-Temporal' 

data_plot.loc['Stride time mean R':'RMS gyr VT R','xaxis'] = np.arange(1,22)

data_plot.loc['Dominant peak freq R':'Dominant peak density R','Type'] = 'Frequency' 
data_plot.loc['Dominant peak freq R':'Dominant peak density R','xaxis'] = np.arange(22,26)

data_plot.loc['ACOV acc AP R':'SampEN VT R','Type'] = 'Complexity' 
data_plot.loc['ACOV acc AP R':'SampEN VT R','xaxis'] = range(40,61)

# low back
data_plot.loc['Step time mean B':'SampEN VT B','Sensor'] = 'lowback'
data_plot.loc['Step time mean B':'Rms gyr VT B','Type'] = 'Spatio-Temporal' 
data_plot.loc['Step time mean B':'Step time norm B','xaxis'] = np.arange(1,4)
data_plot.loc['Range acc AP B':'Rms gyr VT B','xaxis'] = np.arange(10,22)


data_plot.loc['Dominant peak freq AP B':'IH VT B','Type'] = 'Frequency'
data_plot.loc['Dominant peak freq AP B':'IH VT B','xaxis'] = np.arange(22,40)

data_plot.loc['ACOV acc AP B':'SampEN VT B','Type'] = 'Complexity'
data_plot.loc['ACOV acc AP B':'SampEN VT B','xaxis'] = range(40,61) 

# asymmetry
data_plot.loc['SR Swing/stand':,'Sensor'] = 'Combined'
data_plot.loc['SR Swing/stand':,'Type'] = 'asymmetry'
data_plot.loc['SR Swing/stand':,'xaxis'] = range(61,81) 



line1 = sns.lineplot(x = 'xaxis', y = 'ICC', 
                     data = data_plot.loc[data_plot.Type == 'Spatio-Temporal'], 
                     ax=axICC[0,0],marker = '^', 
                     style = 'Type',markersize = 9, palette = 'deep',
                     hue = 'Sensor')

line2 = sns.lineplot(x = 'xaxis', y = 'ICC', 
                     data = data_plot.loc[data_plot.Type == 'Frequency'], 
                     ax=axICC[0,1],marker = '^', 
                     style = 'Type',markersize = 9, palette = 'deep',
                     hue = 'Sensor')

line3 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', 
                     data = data_plot.loc[data_plot.Type == 'Spatio-Temporal'], 
                     ax=axICC[0,0], 
                     label = 'Minimal ICC', 
                     color = 'black')
line4 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', 
                     data = data_plot.loc[data_plot.Type == 'Frequency'], 
                     ax=axICC[0,1], 
                     label = 'Minimal ICC', color = 'black')
        
line1.lines[0].set_linestyle("")
line1.lines[0].set_marker("^")
ms = line1.lines[0].get_markersize()
line1.lines[0].set_markersize(ms * 1.5)

line1.lines[1].set_linestyle("")
ms = line1.lines[1].get_markersize()
line1.lines[1].set_marker("^")
line1.lines[1].set_markersize(ms * 1.2)

line1.lines[2].set_linestyle("")
ms = line1.lines[2].get_markersize()
line1.lines[2].set_marker("^")
line1.lines[2].set_markersize(ms * 1)


line2.lines[0].set_linestyle("")
line2.lines[0].set_marker("^")
ms = line2.lines[0].get_markersize()
line2.lines[0].set_markersize(ms * 1.5)

line2.lines[1].set_linestyle("")
line2.lines[0].set_marker("^")
ms = line2.lines[1].get_markersize()
line2.lines[1].set_markersize(ms * 1.2)

line2.lines[2].set_linestyle("")
line2.lines[0].set_marker("^")
ms = line2.lines[2].get_markersize()
line2.lines[2].set_markersize(ms * 1)
axICC[0,0].get_legend().remove()



a = ticker.MultipleLocator(1)
b = ticker.MultipleLocator(1)

axICC[0,0].xaxis.set_major_locator(a)
axICC[0,1].xaxis.set_major_locator(b)


axICC[0,0].set_ylim((0.48,1.0))
axICC[0,1].set_ylim((0.48,1))
axICC[0,1].set_yticklabels([])
axICC[0,0].set_xticklabels([])
axICC[0,1].set_xticklabels([])

axICC[0,0].set_xlabel('')
axICC[0,0].set_ylabel('ICC')
axICC[0,1].set_xlabel('')
axICC[0,1].set_ylabel('')
axICC[0,0].set_title('Spatio-temporal')
axICC[0,1].set_title('Frequency')

handles, labels = axICC[0,1].get_legend_handles_labels()
display = (1,2,3,6)
axICC[0,1].legend([handle for i,handle in enumerate(handles) if i in display],
      [label for i,label in enumerate(labels) if i in display], loc = 'lower right')


axICC[0,1].legend(["Left Foot", "Right Foot", "Low Back"], 
     loc = 'lower right')

axICC[0,0].legend([handle for i,handle in enumerate(handles) if i in display],
      [label for i,label in enumerate(labels) if i in display], loc = 'lower right')

axICC[0,0].legend(["Left Foot", "Right Foot", "Low Back"], 
     loc = 'lower right')
# Bottom figures
line5 = sns.lineplot(x = 'xaxis', y = 'MDC', 
                     data = data_plot.loc[data_plot.Type == 'Spatio-Temporal'], 
                     ax=axICC[1,0],marker = '^',  
                     style = 'Type',markersize = 9, linewidth = 0, 
                     palette = 'deep',
                     hue = 'Sensor')
line6 = sns.lineplot(x = 'xaxis', y = 'MDC', 
                     data = data_plot.loc[data_plot.Type == 'Frequency'], 
                     ax=axICC[1,1],marker = '^', 
                     style = 'Type',markersize = 9, palette = 'deep',
                     linewidth = 0, hue = 'Sensor')


line5.lines[0].set_linestyle("")
line5.lines[0].set_label('Left foot')
line5.lines[0].set_markersize(ms * 1.5)

line5.lines[1].set_linestyle("")
line5.lines[1].set_label('Right foot')
line5.lines[1].set_markersize(ms * 1.2)

line5.lines[2].set_linestyle("")
line5.lines[2].set_label('Low Back')
line5.lines[2].set_markersize(ms * 1.0)


line6.lines[0].set_linestyle("")
line6.lines[0].set_label('Left foot')
line6.lines[0].set_markersize(ms * 1.5)

line6.lines[1].set_linestyle("")
line6.lines[1].set_label('Right foot')
line6.lines[1].set_markersize(ms * 1.2)

line6.lines[2].set_linestyle("")
line6.lines[2].set_label('Low Back')
line6.lines[2].set_markersize(ms * 1.0)

axICC[1,0].set_ylim((0,2))
axICC[1,1].set_ylim((0,2))


axICC[1,0].get_legend().remove()
axICC[1,1].get_legend().remove()

a = ticker.MultipleLocator(1)
b = ticker.MultipleLocator(1)

axICC[1,0].xaxis.set_major_locator(a)
axICC[1,1].xaxis.set_major_locator(b)

axICC[1,1].set_yticklabels([])
axICC[1,0].set_xlabel('')
axICC[1,0].set_ylabel('MDC expressed as STD')
axICC[1,1].set_xlabel('')
axICC[1,1].set_ylabel('')
axICC[1,0].set_title('')

varNames = xls.iloc[:,0]
for number, value in enumerate(varNames):
    name = varNames.loc[varNames == value].index[0]
    num = number+1
    varNames.iloc[number] = str(name)
    
tmp = varNames[0:21]
for num, var in enumerate(tmp):
    tmp[num] = var.replace(" L", "") 
tD = tmp 

tmp = varNames[107:125]
for num, var in enumerate(tmp):
    tmp[num] = var.replace(" B", "") 
fD = tmp 


#dx = 10/72.; dy = 0/72. 
#offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig1.dpi_scale_trans)
#
## apply offset transform to all x ticklabels.
#for label in axICC[1,0].xaxis.get_majorticklabels():
#    label.set_transform(label.get_transform() + offset)
#for label in axICC[1,1].xaxis.get_majorticklabels():
#    label.set_transform(label.get_transform() + offset)
#for label in axICC[1,2].xaxis.get_majorticklabels():
#    label.set_transform(label.get_transform() + offset)
#            
    
# Spatio-Temporal features
labels = [item.get_text() for item in axICC[1,0].get_xticklabels()]

labels[1] = ''
labels[2:22] = tD
labels[0] = ''
#    labels[22] = ''
    
axICC[1,0].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")


# Frequency features
labels = [item.get_text() for item in axICC[1,1].get_xticklabels()]

labels[1:20] = fD
labels[0] = ''
#labels[19] = ''

axICC[1,1].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")


#    os.chdir(saveTo)
#    plt.savefig('SIT.png', dpi = 600)
#    
#    os.chdir(mainDirectory)
#handles, labels = axICC[1,2].get_legend_handles_labels()
#display = (0,1)
#axICC[1,2].legend(['First measurement'], loc = 'upper right')

#axICC[1].set_title('SIT: Minimal detectable change')

#
#if __name__ == '__main__':
#    plotSIT()











fig2, axICC2 = plt.subplots(2,2,figsize=(25,25),dpi = 110, gridspec_kw={'width_ratios': [(21/41), (20/41)]})
plt.tight_layout()
plt.subplots_adjust(left=0.05, bottom=0.20, right=None, top=0.95, wspace=0.02, hspace=0.05)

line1 = sns.lineplot(x = 'xaxis', y = 'ICC', 
                     data = data_plot.loc[data_plot.Type == 'Complexity'], 
                     ax=axICC2[0,0],marker = '^', 
                     style = 'Type',markersize = 9, palette = 'deep',
                     hue = 'Sensor')

line2 = sns.lineplot(x = 'xaxis', y = 'ICC', 
                     data = data_plot.loc[data_plot.Type == 'asymmetry'], 
                     ax=axICC2[0,1],marker = '^', 
                     style = 'Type',markersize = 9, palette = 'deep',
                     hue = 'Sensor')

line3 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', 
                     data = data_plot.loc[data_plot.Type == 'Complexity'], 
                     ax=axICC2[0,0], 
                     label = 'Minimal ICC', 
                     color = 'black')
line4 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', 
                     data = data_plot.loc[data_plot.Type == 'asymmetry'], 
                     ax=axICC2[0,1], 
                     label = 'Minimal ICC', color = 'black')

line1.lines[0].set_linestyle("")
ms = line1.lines[0].get_markersize()
line1.lines[0].set_markersize(ms * 1.5)

line1.lines[1].set_linestyle("")
ms = line1.lines[1].get_markersize()
line1.lines[1].set_markersize(ms * 1.2)

line1.lines[2].set_linestyle("")
ms = line1.lines[2].get_markersize()
line1.lines[2].set_markersize(ms * 1)


line2.lines[0].set_linestyle("")
ms = line2.lines[0].get_markersize()
line2.lines[0].set_markersize(ms * 1.5)

line2.lines[1].set_linestyle("")
ms = line2.lines[1].get_markersize()
line2.lines[1].set_markersize(ms * 1.2)

line2.lines[2].set_linestyle("")
ms = line2.lines[2].get_markersize()
line2.lines[2].set_markersize(ms * 1)
axICC2[0,0].get_legend().remove()



a = ticker.MultipleLocator(1)
b = ticker.MultipleLocator(1)

axICC2[0,0].xaxis.set_major_locator(a)
axICC2[0,1].xaxis.set_major_locator(b)


axICC2[0,0].set_ylim((0.48,1.0))
axICC2[0,1].set_ylim((0.48,1))
axICC2[0,1].set_yticklabels([])
axICC2[0,0].set_xticklabels([])
axICC2[0,1].set_xticklabels([])

axICC2[0,0].set_xlabel('')
axICC2[0,0].set_ylabel('ICC')
axICC2[0,1].set_xlabel('')
axICC2[0,1].set_ylabel('')
axICC2[0,0].set_title('Complexity')
axICC2[0,1].set_title('Asymmetry')


# Bottom figures
line5 = sns.lineplot(x = 'xaxis', y = 'MDC', 
                     data = data_plot.loc[data_plot.Type == 'Complexity'], 
                     ax=axICC2[1,0],marker = '^',  
                     style = 'Type',markersize = 9, linewidth = 0, 
                     palette = 'deep',
                     hue = 'Sensor')
line6 = sns.lineplot(x = 'xaxis', y = 'MDC', 
                     data = data_plot.loc[data_plot.Type == 'asymmetry'], 
                     ax=axICC2[1,1],marker = '^', 
                     style = 'Type',markersize = 9, palette = 'deep',
                     linewidth = 0, hue = 'Sensor')

ms = line5.lines[0].get_markersize()
line5.lines[0].set_linestyle("")
line5.lines[0].set_label('Left foot')
line5.lines[0].set_markersize(ms * 1.5)

line5.lines[1].set_linestyle("")
line5.lines[1].set_label('Right foot')
line5.lines[1].set_markersize(ms * 1.2)

line5.lines[2].set_linestyle("")
line5.lines[2].set_label('Low Back')
line5.lines[2].set_markersize(ms * 1.0)


line6.lines[0].set_linestyle("")
line6.lines[0].set_label('Left foot')
line6.lines[0].set_markersize(ms * 1.5)

line6.lines[1].set_linestyle("")
line6.lines[1].set_label('Right foot')
line6.lines[1].set_markersize(ms * 1.2)

line6.lines[2].set_linestyle("")
line6.lines[2].set_label('Low Back')
line6.lines[2].set_markersize(ms * 1.0)


axICC2[1,0].set_ylim((0,2))
axICC2[1,1].set_ylim((0,2))

axICC2[0,1].get_legend().remove()
axICC2[1,0].get_legend().remove()
axICC2[1,1].get_legend().remove()

a = ticker.MultipleLocator(1)
b = ticker.MultipleLocator(1)

axICC2[1,0].xaxis.set_major_locator(a)
axICC2[1,1].xaxis.set_major_locator(b)

axICC2[1,1].set_yticklabels([])
axICC2[1,0].set_xlabel('')
axICC2[1,0].set_ylabel('MDC expressed as STD')
axICC2[1,1].set_xlabel('')
axICC2[1,1].set_ylabel('')
axICC2[1,0].set_title('')

tmp = varNames[25:46]
for num, var in enumerate(tmp):
    tmp[num] = var.replace(" L", "") 
c  = tmp 

a = varNames[146:166]

#dx = 10/72.; dy = 0/72. 
#offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig1.dpi_scale_trans)
#
## apply offset transform to all x ticklabels.
#for label in axICC2[1,0].xaxis.get_majorticklabels():
#    label.set_transform(label.get_transform() + offset)
#for label in axICC2[1,1].xaxis.get_majorticklabels():
#    label.set_transform(label.get_transform() + offset)
#for label in axICC2[1,2].xaxis.get_majorticklabels():
#    label.set_transform(label.get_transform() + offset)
#            
    
# Spatio-Temporal features
labels = [item.get_text() for item in axICC2[1,0].get_xticklabels()]

labels[1] = ''
labels[2:25] = c
labels[0] = ''
#    labels[22] = ''
    
axICC2[1,0].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")


# Frequency features
labels = [item.get_text() for item in axICC2[1,1].get_xticklabels()]

labels[1:20] = a
labels[0] = ''
#labels[19] = ''

axICC2[1,1].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")


axICC2[0,0].legend([handle for i,handle in enumerate(handles) if i in display],
      [label for i,label in enumerate(labels) if i in display], loc = 'lower right')

axICC2[0,0].legend(["Left foot", "Right foot", "Low Back"], 
     loc = 'lower right')

axICC2[0,1].legend(["Asymmetry"], 
     loc = 'lower right')






# Average ICC LeftFoot and rightFoot

LST = data_plot.loc[(data_plot['Sensor'] == 'leftfoot') & 
                        (data_plot['Type'] == 'Spatio-Temporal'), 'ICC'].mean()

LF = data_plot.loc[(data_plot['Sensor'] == 'leftfoot') & 
                        (data_plot['Type'] == 'Frequency'), 'ICC'].mean()

LC = data_plot.loc[(data_plot['Sensor'] == 'leftfoot') & 
                        (data_plot['Type'] == 'Complexity'), 'ICC'].mean()

print(f'Left foot: ST {LST}, F{LF}, LC{LC}')

RST = data_plot.loc[(data_plot['Sensor'] == 'rightfoot') & 
                        (data_plot['Type'] == 'Spatio-Temporal'), 'ICC'].mean()

RF = data_plot.loc[(data_plot['Sensor'] == 'rightfoot') & 
                        (data_plot['Type'] == 'Frequency'), 'ICC'].mean()

RC = data_plot.loc[(data_plot['Sensor'] == 'rightfoot') & 
                        (data_plot['Type'] == 'Complexity'), 'ICC'].mean()

print(f'right foot: ST {RST}, F{RF}, LC{RC}')


