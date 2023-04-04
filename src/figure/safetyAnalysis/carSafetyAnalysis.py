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

root_path = os.path.abspath('../../../')

font1 = {
    'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 16,
}

fontlegend = {
    'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 16,
}

data_path100m = root_path + "/asset/mergingData100m.csv"
data_path150m = root_path + "/asset/mergingData150m.csv"
data_path200m = root_path + "/asset/mergingData200m.csv"

ori_data100m = pd.read_csv(data_path100m)
ori_data150m = pd.read_csv(data_path150m)
ori_data200m = pd.read_csv(data_path200m)

TTC_THRESHOLD = 15

mergingData100m = ori_data100m[
    (ori_data100m['MergingState'] == True)
    & (ori_data100m['RouteClass'] == 'entry')
    & (ori_data100m['BreakRuleState'] == 'None')
    & (ori_data100m['MergingDistance'] != 'None')
    & (ori_data100m['MaxLateralSpeed'] != 'None')
    & (ori_data100m['MergingType'] != 'None')
    & (ori_data100m['MergingType'] != 'G')
    & (ori_data100m['MergingType'] != 'H')
    ]
mergingData100m['miniTTC'] = mergingData100m.loc[:, ['MiniRearTTC', 'MiniLeadTTC']].min(axis=1)
mergingData100m = mergingData100m[mergingData100m["miniTTC"] < TTC_THRESHOLD]

mergingData150m = ori_data150m[
    (ori_data150m['MergingState'] == True)
    & (ori_data150m['RouteClass'] == 'entry')
    & (ori_data150m['BreakRuleState'] == 'None')
    & (ori_data150m['MergingDistance'] != 'None')
    & (ori_data150m['MaxLateralSpeed'] != 'None')
    & (ori_data150m['MergingType'] != 'None')
    & (ori_data150m['MergingType'] != 'G')
    & (ori_data150m['MergingType'] != 'H')
    ]
mergingData150m['miniTTC'] = mergingData150m.loc[:, ['MiniRearTTC', 'MiniLeadTTC']].min(axis=1)
mergingData150m = mergingData150m[mergingData150m["miniTTC"] < TTC_THRESHOLD]

mergingData200m = ori_data200m[
    (ori_data200m['MergingState'] == True)
    & (ori_data200m['RouteClass'] == 'entry')
    & (ori_data200m['BreakRuleState'] == 'None')
    & (ori_data200m['MergingDistance'] != 'None')
    & (ori_data200m['MaxLateralSpeed'] != 'None')
    & (ori_data200m['MergingType'] != 'None')
    & (ori_data200m['MergingType'] != 'G')
    & (ori_data200m['MergingType'] != 'H')
    ]
mergingData200m['miniTTC'] = mergingData200m.loc[:, ['MiniRearTTC', 'MiniLeadTTC']].min(axis=1)
mergingData200m = mergingData200m[mergingData200m["miniTTC"] < TTC_THRESHOLD]

mergingData100m.sort_values(by="MergingType", inplace=True)
mergingData150m.sort_values(by="MergingType", inplace=True)
mergingData200m.sort_values(by="MergingType", inplace=True)

FONTSIZE = 16
plt.figure(figsize=(14, 10))
plt.style.use('seaborn-colorblind')

j = 0
for i in [2,3,5,6]:
    curlocation100m = mergingData100m[mergingData100m["location"]==i]
    curlocation150m = mergingData150m[mergingData150m["location"]==i]
    curlocation200m = mergingData200m[mergingData200m["location"]==i]
    curlocation100m["DISTANCE"] = 100
    curlocation150m["DISTANCE"] = 150
    curlocation200m["DISTANCE"] = 200

    totalData = pd.concat([curlocation100m, curlocation150m,curlocation200m], axis=0)

    ax1 = plt.subplot(2, 2, j+1)
    g1 = sns.barplot(x="MergingType", y="miniTTC", hue="DISTANCE", data=totalData[totalData["vehicleClass"]=="car"],palette="hls")
    g1.set(xlabel=None)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,2,4,6,8,10,12,14,16,18,20])
    plt.ylabel("TTC(s)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+", car", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    j += 1

plt.tight_layout()
plt.savefig(root_path+"/asset/safetyAnalysis/carTTCBarplot.png", dpi=800)
