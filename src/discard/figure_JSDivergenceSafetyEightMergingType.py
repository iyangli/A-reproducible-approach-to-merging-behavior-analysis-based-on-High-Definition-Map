import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import scipy.stats
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

data_path100m = root_path + "/asset/mergingData100m.csv"
data_path150m = root_path + "/asset/mergingData150m.csv"
data_path200m = root_path + "/asset/mergingData200m.csv"

ori_data100m = pd.read_csv(data_path100m)
ori_data150m = pd.read_csv(data_path150m)
ori_data200m = pd.read_csv(data_path200m)

TTC_THRESHOLD = 50

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


mergingData100m['miniTTC'] = mergingData100m['miniTTC'].astype('float')
mergingData150m['miniTTC'] = mergingData150m['miniTTC'].astype('float')
mergingData200m['miniTTC'] = mergingData200m['miniTTC'].astype('float')

def JS_divergence(p,q):
    M=(p+q)/2
    return 0.5*scipy.stats.entropy(p, M, base=2)+0.5*scipy.stats.entropy(q, M, base=2)

def JS_div(arr1,arr2,num_bins):
    max0 = max(np.max(arr1),np.max(arr2))
    min0 = min(np.min(arr1),np.min(arr2))
    bins = np.linspace(0,15, num=num_bins)
    PDF1 = pd.cut(arr1,bins,duplicates="drop").value_counts() / len(arr1)
    PDF2 = pd.cut(arr2,bins,duplicates="drop").value_counts() / len(arr2)


    print(PDF2)

    return JS_divergence(PDF1.values,PDF2.values)

num_bins = 30
mergingType = ["B","C","D","E","F"]
locationDic ={}

print(np.unique(mergingData100m["MergingType"].values))

print(mergingData100m[mergingData100m["MergingType"]=="B"])

for curLocation in [2,3,5,6]:

    curlocation100m = mergingData100m[(mergingData100m["location"] == curLocation) ]
    curlocation150m = mergingData150m[(mergingData150m["location"] == curLocation) ]
    curlocation200m = mergingData200m[(mergingData200m["location"] == curLocation) ]

    curLocation100m, curLocation150m, curLocation200m = [],[],[]

    for i in mergingType:
        JS100list, JS150list, JS200list =[], [], []

        curRow100m = curlocation100m[curlocation100m["MergingType"] == i ]
        curRow150m = curlocation150m[curlocation150m["MergingType"] == i ]
        curRow200m = curlocation200m[curlocation200m["MergingType"] == i ]
        print(i)

        print(curRow100m)

        for j in mergingType:
            curColumn100m = curlocation100m[curlocation100m["MergingType"] == j ]
            curColumn150m = curlocation150m[curlocation150m["MergingType"] == j ]
            curColumn200m = curlocation200m[curlocation200m["MergingType"] == j ]

            JS100m = JS_div(curRow100m["miniTTC"].values,curColumn100m["miniTTC"].values,num_bins = num_bins)
            JS150m = JS_div(curRow150m["miniTTC"].values,curColumn150m["miniTTC"].values,num_bins = num_bins)
            JS200m = JS_div(curRow200m["miniTTC"].values,curColumn200m["miniTTC"].values,num_bins = num_bins)

            JS100list.append(JS100m)
            JS150list.append(JS150m)
            JS200list.append(JS200m)

        curLocation100m.append(JS100list)
        curLocation150m.append(JS150list)
        curLocation200m.append(JS200list)

    locationDic[str(curLocation)] = [curLocation100m,curLocation150m,curLocation200m]

mask=np.zeros_like(locationDic["2"][2])
for i in range(1,len(mask)):
    for j in range(0,i):
        mask[j][i]=True


FONTSIZE = 16
plt.figure(figsize=(22, 12))
plt.style.use('seaborn-colorblind')

j = 0

for k in [2,3,5,6]:

    ax1 = plt.subplot(4,3,3*j+1)
    sns.heatmap(locationDic[str(k)][0], cmap='coolwarm',mask = mask, annot=True, center=0, linewidths=0.8,vmin=0,vmax=1, fmt='.2f', cbar=False, annot_kws={"fontsize":16})
    sns.set_context("notebook")
    plt.grid(ls='--', axis="both")
    plt.style.use('seaborn-colorblind')
    ax1.set_xticklabels(mergingType, fontsize=18, horizontalalignment='right')
    ax1.set_yticklabels(mergingType, fontsize=18, horizontalalignment='right')
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("DISTANCE=100,location" + str(k), font1)

    ax2 = plt.subplot(4,3,3*j+2)
    sns.heatmap(locationDic[str(k)][1], cmap='coolwarm',mask = mask, annot=True, center=0, linewidths=0.8,vmin=0,vmax=1, fmt='.2f', cbar=False, annot_kws={"fontsize":16})
    sns.set_context("notebook")
    plt.grid(ls='--', axis="both")
    plt.style.use('seaborn-colorblind')
    ax2.set_xticklabels(mergingType, fontsize=18, horizontalalignment='right')
    ax2.set_yticklabels(mergingType, fontsize=18, horizontalalignment='right')
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("DISTANCE=150,location" + str(k), font1)

    ax3 = plt.subplot(4,3,3*j+3)
    sns.heatmap(locationDic[str(k)][2], cmap='coolwarm',mask = mask, annot=True, center=0, linewidths=0.8,vmin=0,vmax=1, fmt='.2f', cbar=False, annot_kws={"fontsize":16})
    sns.set_context("notebook")
    plt.grid(ls='--', axis="both")
    plt.style.use('seaborn-colorblind')
    ax3.set_xticklabels(mergingType, fontsize=18, horizontalalignment='right')
    ax3.set_yticklabels(mergingType, fontsize=18, horizontalalignment='right')
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("DISTANCE=200,location" + str(k), font1)

    j += 1

plt.tight_layout()
# plt.show()
plt.savefig(root_path+"/asset/figure_JSHeatmapMiniTTCEightMergingType.png", dpi=500)
# plt.clf()
