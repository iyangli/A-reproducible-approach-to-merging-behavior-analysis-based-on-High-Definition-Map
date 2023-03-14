import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')
pd.set_option('max_colwidth',200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

root_path = os.path.abspath('../../')

font1 = {
    'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 16,
}

fontlegend = {
    'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 14,
}

FONTSIZE = 16
plt.figure(figsize=(12, 10))
plt.style.use('seaborn-colorblind')

data_path = root_path + "/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[
    (ori_data['MergingState']==True)
    & (ori_data['RouteClass']=='entry')
    & (ori_data['BreakRuleState']=='None')
    & (ori_data['MergingDistance'] !='None')
    & (ori_data['MaxLateralSpeed'] !='None')
    & (ori_data['MergingType'] != 'None')
    & (ori_data['MergingType'] != 'G')
    & (ori_data['MergingType'] != 'H')
    ]

mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))

employedColumns = ['MergingDistanceRatio', 'MergingDuration',
                   'trafficFlowArea4', 'trafficSpeedArea4',
                   'trafficFlowArea5',  'trafficSpeedArea5']

# employedColumns = ['MergingDistanceRatio', 'totalvelocity', 'MergingDuration', "MaxLateralSpeed", "MaxiLateralAcc",
#                    'trafficFlowArea4', 'trafficDensityArea4', 'trafficSpeedArea4',
#                    'trafficFlowArea5', 'trafficDensityArea5', 'trafficSpeedArea5']

mergingData.sort_values(by="vehicleClass", inplace=True)
data = mergingData[ (mergingData["location"]==2)]

plt.subplots(figsize=(30, 10))
ax1 = plt.subplot(1,6,1)
g1 = sns.heatmap(data[data["MergingType"] == "A"][employedColumns].corr(), cmap='YlGnBu', annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False,ax=ax1)
plt.ylabel("Speed(m/s)", font1)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax1.set_xticklabels([], fontsize = 18, horizontalalignment='right')
# ax1.set_yticklabels([], fontsize = 18, horizontalalignment='right')

ax2 = plt.subplot(1,6,2)
g2 = sns.heatmap(data[data["MergingType"] == "B"][employedColumns].corr(), cmap='YlGnBu', annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False,ax=ax2)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax2.set_xticklabels([], fontsize = 18, horizontalalignment='right')
ax2.set_yticklabels([], fontsize = 18, horizontalalignment='right')

ax3 = plt.subplot(1,6,3)
g3 = sns.heatmap(data[data["MergingType"] == "C"][employedColumns].corr(), cmap='YlGnBu', annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False,ax=ax3)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax3.set_xticklabels([], fontsize = 18, horizontalalignment='right')
ax3.set_yticklabels([], fontsize = 18, horizontalalignment='right')

ax4 = plt.subplot(1,6,4)
g4 = sns.heatmap(data[data["MergingType"] == "D"][employedColumns].corr(), cmap='YlGnBu', annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False,ax=ax4)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax4.set_xticklabels([], fontsize = 18, horizontalalignment='right')
ax4.set_yticklabels([], fontsize = 18, horizontalalignment='right')

ax5 = plt.subplot(1,6,5)
g5 = sns.heatmap(data[data["MergingType"] == "E"][employedColumns].corr(), cmap='YlGnBu', annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False,ax=ax5)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax5.set_xticklabels([], fontsize = 18, horizontalalignment='right')
ax5.set_yticklabels([], fontsize = 18, horizontalalignment='right')

ax6 = plt.subplot(1,6,6)
g6 = sns.heatmap(data[data["MergingType"] == "F"][employedColumns].corr(), cmap='YlGnBu', annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False,ax=ax6)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax6.set_xticklabels([], fontsize = 18, horizontalalignment='right')
ax6.set_yticklabels([], fontsize = 18, horizontalalignment='right')

plt.tight_layout()
plt.show()
# plt.savefig(root_path+"/asset/figure_MacroscopicEightMergingType.png", dpi=800)
# plt.clf()
