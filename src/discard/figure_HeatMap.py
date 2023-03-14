import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings('ignore')

font1 = {
    'family': 'Times New Roman',
    'weight': 'normal',
    'size': 14,
}

root_path = os.path.abspath('../../')
data_path = root_path + "/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[(ori_data['MergingState'] == True)
                       & (ori_data['RouteClass'] == 'entry')
                       & (ori_data['BreakRuleState'] == 'None')
                       & (ori_data['MergingDistance'] != 'None')
                       & (ori_data['MaxLateralSpeed'] != 'None')
                       ]

mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity']) + np.square(mergingData['yVelocity']))
mergingData.sort_values(by="vehicleClass", inplace=True)


FONTSIZE = 14
plt.figure(figsize=(8, 6))

employedColumns = ['MergingDistanceRatio', 'totalvelocity', 'MergingDuration', "MaxLateralSpeed", "MaxiLateralAcc",
                   'trafficFlowArea4', 'trafficDensityArea4', 'trafficSpeedArea4',
                   'trafficFlowArea5', 'trafficDensityArea5', 'trafficSpeedArea5']

location2 = mergingData[mergingData["location"] == 2]
location3 = mergingData[mergingData["location"] == 3]
location5 = mergingData[mergingData["location"] == 5]
location6 = mergingData[mergingData["location"] == 6]

location2 = location2[location2["vehicleClass"] == "van"]

data = location2[employedColumns]
spearman_table = data.corr("spearman")

mask = np.zeros_like(data.corr(), dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

mask2 = np.abs(spearman_table) <= 0.1
mask = mask | mask2

plt.subplots(figsize=(10, 10))

sns.heatmap(data.corr(), cmap='YlGnBu', mask=mask, annot=True, center=0, linewidths=0.8,vmin=-1,vmax=1, fmt='.2f', cbar=False)
plt.xlabel("a) Location", font1)
plt.ylabel("Speed(m/s)", font1)
plt.title("Merging Speed", font1)
sns.set_context("notebook")
plt.grid(ls='--', axis="both")
plt.style.use('seaborn-colorblind')

plt.show()

# plt.savefig(root_path+"/asset/figure8_.png", dpi=600)
