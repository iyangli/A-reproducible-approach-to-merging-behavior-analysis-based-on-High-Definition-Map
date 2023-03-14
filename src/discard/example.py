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


statistc = pd.DataFrame()

for i in [100,150,200]:

    data_path = root_path+"/asset/mergingData"+str(i)+"m.csv"
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
            curDic["DISTANCE"] = i
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

            statistc = pd.concat([statistc, pd.DataFrame([curDic])], axis=0)

# statistc.to_excel(root_path+"/asset/table/trafficFlowSpeed.xlsx")

FONTSIZE = 16
plt.figure(figsize=(12, 8))
plt.style.use('seaborn-colorblind')
j = 0

data_path = root_path + "/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[
    (ori_data['MergingState'] == True)
    & (ori_data['RouteClass'] == 'entry')
    & (ori_data['BreakRuleState'] == 'None')
    & (ori_data['MergingDistance'] != 'None')
    & (ori_data['MaxLateralSpeed'] != 'None')
    & (ori_data['MergingType'] != 'None')
    ]

mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData.sort_values(by="vehicleClass", inplace=True)


ax1 = plt.subplot(2,2,1)
g1 = sns.scatterplot(x="trafficDensityArea4", y="trafficFlowArea4", data=mergingData[mergingData["location"]==3], palette="Paired_r",alpha=0.8)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,500,1000,1500,2000,2500])
plt.ylabel("flow(veh/h)", font1)
plt.xlabel("density(veh/km)", font1)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.title("Upstream traffic flow and space-mean speed ", font1)

ax2 = plt.subplot(2,2,2)
curstatistic = statistc[statistc["DISTANCE"]==100]
curstatisticlocation2 = curstatistic[curstatistic["location"]==3]
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.plot(curstatisticlocation2["trafficFlowArea4"].values,'-',linewidth =2.5, label="2", alpha=0.9)
plt.xticks([0,1,2,3,4,5], ["A","B","C","D","E","F"])
plt.ylabel("flow(veh/h)", font1)
plt.xlabel("merging scenario", font1)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.title("Upstream traffic flow and space-mean speed ", font1)

ax3 = plt.subplot(2,2,3)
g3 = sns.scatterplot(x="trafficDensityArea5", y="trafficFlowArea5", data=mergingData[mergingData["location"]==3],  palette="Paired_r",alpha=0.8)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,500,1000,1500,2000,2500])
plt.ylabel("flow(veh/h)", font1)
plt.xlabel("density(veh/km)", font1)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.title("Downstream traffic flow and space-mean speed ", font1)

ax4 = plt.subplot(2,2,4)
plt.plot(curstatisticlocation2["trafficFlowArea5"].values,'-',linewidth =2.5, label="2", alpha=0.9)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.xlabel("merging scenario", font1)
plt.xticks([0,1,2,3,4,5], ["A","B","C","D","E","F"])
plt.ylabel("flow(veh/h)", font1)
plt.grid(ls='-', axis="both")
plt.title("Downstream traffic flow and space-mean speed ", font1)
sns.set_context("notebook")

plt.tight_layout()
# plt.show()
plt.savefig(root_path+"/asset/trafficFlowSpeed/trafficSpeedFlowexample.png", dpi=400)
# plt.clf()
