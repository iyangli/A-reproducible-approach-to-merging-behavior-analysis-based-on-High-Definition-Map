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
'size'   : 14,
}


statistic = pd.DataFrame()

data_path = root_path + "/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[
    (ori_data['MergingState']==True)
    & (ori_data['RouteClass']=='entry')
    & (ori_data['BreakRuleState']=='None')
    & (ori_data['MergingDistance'] !='None')
    & (ori_data['MaxLateralSpeed'] !='None')
    & (ori_data['MergingType'] != 'None')
    ]

mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))

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

    mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
    mergingData.sort_values(by="MergingType", inplace=True)

    ax1 = plt.subplot(4, 4, 4 * j + 1)
    g1 = sns.scatterplot(x="trafficDensityArea4", y="trafficFlowArea4", data=mergingData[mergingData["location"]==i],hue = "MergingType",palette="Paired_r",style="MergingType",size="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,300,600,900,1200,1500,1800,2100,2400])
    plt.ylim([0,2400])
    plt.xticks([0,5,10,15,20,25,30,35])
    plt.ylabel("flow(veh/h)", font1)
    plt.xlabel("density(veh/km)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Upstream-Flow-Density", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    ax2 = plt.subplot(4, 4, 4 * j + 2)
    g2 = sns.scatterplot(x="trafficFlowArea4", y="trafficSpeedArea4", data=mergingData[mergingData["location"]==i], hue = "MergingType",palette="Paired_r",style="MergingType",size="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.xticks([0,300,600,900,1200,1500,1800,2100,2400])
    plt.yticks([0,20,40,60,80,100,120,140,160])
    plt.xlim([0,2400])
    plt.xlabel("flow(veh/h)", font1)
    plt.ylabel("speed(m/s)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Upstream-Flow-Speed", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    ax3 = plt.subplot(4, 4, 4 * j + 3)
    g3 = sns.scatterplot(x="trafficDensityArea5", y="trafficFlowArea5", data=mergingData[mergingData["location"]==i], hue = "MergingType",palette="Paired_r",style="MergingType",size="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0,300,600,900,1200,1500,1800,2100,2400])
    plt.ylim([0,2400])
    plt.xticks([0,5,10,15,20,25,30,35])
    plt.ylabel("flow(veh/h)", font1)
    plt.xlabel("density(veh/km)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Downstream-Flow-Density", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    ax4 = plt.subplot(4, 4, 4 * j + 4)
    g4 = sns.scatterplot(x="trafficFlowArea5", y="trafficSpeedArea5", data=mergingData[mergingData["location"]==i], hue = "MergingType",palette="Paired_r",style="MergingType",size="MergingType")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.xticks([0,300,600,900,1200,1500,1800,2100,2400])
    plt.yticks([0,20,40,60,80,100,120,140,160])
    plt.xlim([0,2400])
    plt.xlabel("flow(veh/h)", font1)
    plt.ylabel("speed(m/s)", font1)
    plt.grid(ls='-', axis="both")
    plt.title("location" + str(i)+"-Downstream-Flow-Speed", font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    if j !=0:
        ax1.get_legend().remove()
        ax2.get_legend().remove()
        ax3.get_legend().remove()
        ax4.get_legend().remove()

    j += 1

plt.tight_layout()
# plt.show()
plt.savefig(root_path+"/asset/trafficFlowSpeed/trafficSpeedFlowScatter.png", dpi=400)
# plt.clf()
