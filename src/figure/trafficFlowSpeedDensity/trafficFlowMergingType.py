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

FONTSIZE = 16
plt.figure(figsize=(12, 6))
plt.style.use('seaborn-colorblind')

curstatisticlocation2 = statistic[statistic["location"]==2]
curstatisticlocation3 = statistic[statistic["location"]==3]
curstatisticlocation5 = statistic[statistic["location"]==5]
curstatisticlocation6 = statistic[statistic["location"]==6]

flowArea4 = [curstatisticlocation2["trafficFlowArea4"].values,curstatisticlocation3["trafficFlowArea4"].values,
             curstatisticlocation5["trafficFlowArea4"].values,curstatisticlocation6["trafficFlowArea4"].values]

flowArea5 = [curstatisticlocation2["trafficFlowArea5"].values,curstatisticlocation3["trafficFlowArea5"].values,
             curstatisticlocation5["trafficFlowArea5"].values,curstatisticlocation6["trafficFlowArea5"].values]

ax1 = plt.subplot(1,2,1)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.plot(curstatisticlocation2["trafficFlowArea4"].values,'-',linewidth =2.5, label="location2", alpha=0.9, marker='o')
plt.plot(curstatisticlocation3["trafficFlowArea4"].values,'--',linewidth =2.5,label="location3", alpha=0.9, marker='+')
plt.plot(curstatisticlocation5["trafficFlowArea4"].values,'-.',linewidth =2.5,label="location5", alpha=0.9, marker='*')
plt.plot(curstatisticlocation6["trafficFlowArea4"].values,'o--',linewidth =2.5,label="location6", alpha=0.9, marker='d')
plt.plot(np.mean(flowArea4,axis=0),color="red",linewidth =2.5,label="average", alpha=0.9, marker='s')
plt.xticks([0,1,2,3,4,5], ["A","B","C","D","E","F"])
plt.yticks([0,200,400,600,800,1000,1200,1400])
plt.ylabel("flow(veh/h)", font1)
plt.xlabel("merging scenario", font1)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.title("upstream traffic flow", font1)
plt.legend(prop=fontlegend)

ax2 = plt.subplot(1,2,2)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.plot(curstatisticlocation2["trafficFlowArea5"].values,'-',linewidth =2.5, label="location2", alpha=0.9, marker='o')
plt.plot(curstatisticlocation3["trafficFlowArea5"].values,'--',linewidth =2.5,label="location3", alpha=0.9, marker='+')
plt.plot(curstatisticlocation5["trafficFlowArea5"].values,'-.',linewidth =2.5,label="location5", alpha=0.9, marker='*')
plt.plot(curstatisticlocation6["trafficFlowArea5"].values,'o--',linewidth =2.5,label="location6", alpha=0.9, marker='d')
plt.plot(np.mean(flowArea5,axis=0),color="red",linewidth =2.5,label="average", alpha=0.9, marker='s')
plt.xticks([0,1,2,3,4,5], ["A","B","C","D","E","F"])
plt.yticks([0,200,400,600,800,1000,1200,1400])
plt.ylabel("flow(veh/h)", font1)
plt.xlabel("merging scenario", font1)
plt.grid(ls='-', axis="both")
sns.set_context("notebook")
plt.legend(prop=fontlegend)
ax2.get_legend().remove()
plt.title("downstream traffic flow", font1)

plt.tight_layout()
plt.savefig(root_path+"/asset/trafficFlowSpeed/trafficFlowMergingType.png", dpi=400)
