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
import scipy
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

statistic = pd.DataFrame()
data_path = root_path + "/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[
    (ori_data['MergingState'] == True)
    & (ori_data['RouteClass'] == 'entry')
    & (ori_data['BreakRuleState'] == 'None')
    & (ori_data['MergingDistance'] != 'None')
    & (ori_data['MaxLateralSpeed'] != 'None')
    & (ori_data['MergingType'] != 'None')
    & (ori_data['MergingType'] != 'G')
    & (ori_data['MergingType'] != 'H')
    & (ori_data['MergingType'] != 'A')
    & (ori_data['vehicleClass'] == 'car')
    # & (ori_data['MergingType'] != 'B')
    # & (ori_data['MergingType'] != 'D')
    # & (ori_data['MergingType'] != 'C')
    ]

employedColumns = ['MergingDistanceRatio', 'totalvelocity', 'MergingDuration',
                   'trafficFlowArea4','trafficFlowArea5',"MergingType" ]

mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))
mergingData.sort_values(by="MergingType", inplace=True)

for curLocation, curLocationGroup in mergingData.groupby("location"):
    for curMergingType, curMergingTypeGroup in curLocationGroup.groupby("MergingType"):
        curDic = {}
        curDic["location"] = curLocation
        curDic["MergingType"] = curMergingType
        if curMergingType =="G" or curMergingType =="H":
            continue
        curDic["trafficFlowArea4"] = np.mean(curMergingTypeGroup["trafficFlowArea4"])
        curDic["trafficFlowArea5"] = np.mean(curMergingTypeGroup["trafficFlowArea5"])
        curDic["trafficDensityArea4"] = np.mean(curMergingTypeGroup["trafficDensityArea4"])
        curDic["trafficDensityArea5"] = np.mean(curMergingTypeGroup["trafficDensityArea5"])
        curDic["trafficSpeedArea4"] = np.mean(curMergingTypeGroup["trafficSpeedArea4"])
        curDic["trafficSpeedArea5"] = np.mean(curMergingTypeGroup["trafficSpeedArea5"])
        statistic = pd.concat([statistic, pd.DataFrame([curDic])], axis=0)

FONTSIZE = 14
plt.figure(figsize=(24, 16))
plt.style.use('seaborn-colorblind')
j = 0

for i in [2,3,5,6]:

    ax1 = plt.subplot(4, 4, 4 * j + 1)
    g1 = sns.scatterplot(x="MergingDistanceRatio", y="trafficFlowArea4", data=mergingData[mergingData["location"]==i],hue = "MergingType",palette="Paired_r",style="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000])
    plt.ylim([0,2000])
    plt.xticks([0,0.2,0.4,0.6,0.8,1])
    plt.ylabel("flow(veh/h)", font1)
    plt.xlabel("distance ratio", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Upstream", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend,ncol=2)

    ax2 = plt.subplot(4, 4, 4 * j + 2)
    g2 = sns.scatterplot(x="MergingDuration", y="trafficFlowArea4", data=mergingData[mergingData["location"]==i],hue = "MergingType",palette="Paired_r",style="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000])
    plt.ylim([0,2000])
    plt.xticks([0,2,4,6,8,10])
    plt.xlim([0,10])
    plt.ylabel("flow(veh/h)", font1)
    plt.xlabel("duration(s)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Upstream", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend,ncol=2)

    ax3 = plt.subplot(4, 4, 4 * j + 3)
    g3 = sns.scatterplot(x="MergingDistanceRatio", y="trafficFlowArea5", data=mergingData[mergingData["location"]==i],hue = "MergingType",palette="Paired_r",style="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000])
    plt.ylim([0,2000])
    plt.xticks([0,0.2,0.4,0.6,0.8,1])
    plt.ylabel("flow(veh/h)", font1)
    plt.xlabel("distance ratio", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Downstream", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend,ncol=2)

    ax4 = plt.subplot(4, 4, 4 * j + 4)
    g4 = sns.scatterplot(x="MergingDuration", y="trafficFlowArea5", data=mergingData[mergingData["location"]==i], hue = "MergingType",palette="Paired_r",style="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,200,400,600,800,1000,1200,1400,1600,1800,2000])
    plt.ylim([0,2000])
    plt.xticks([0,2,4,6,8,10])
    plt.xlim([0,10])
    plt.ylabel("flow(veh/h)", font1)
    plt.xlabel("duration(s)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Downstream", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend,ncol=2)

    if j !=0:
        ax1.get_legend().remove()
        ax2.get_legend().remove()
        ax3.get_legend().remove()
        ax4.get_legend().remove()

    j += 1

plt.tight_layout()
# plt.show()
plt.savefig(root_path+"/asset/trafficFlowSpeed/trafficFlowDistanceRatioDurationScatter.png", dpi=400)
# plt.clf()
