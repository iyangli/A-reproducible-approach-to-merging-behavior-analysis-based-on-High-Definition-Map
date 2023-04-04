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
        for curVehicleClass, curVehicleGroup in curLocationGroup.groupby("vehicleClass"):
            for curMergingType, curMergingTypeGroup in curVehicleGroup.groupby("MergingType"):
                consecutive = curMergingTypeGroup[curMergingTypeGroup["LaneChangingCounts"]==2]
                consecutive["ConsecutiveDuration"]  = consecutive['ConsecutiveDuration'].astype('float')
                curDic = {}
                curDic["DISTANCE"] = i
                curDic["location"] = curLocation
                curDic["vehicleClass"] = curVehicleClass
                curDic["MergingType"] = curMergingType
                curDic["Count"] = len(consecutive)
                curDic["PercentMergingType"] = len(consecutive)/len(curMergingTypeGroup)
                if len(consecutive)/len(curMergingTypeGroup) != 0:
                    curDic["ConsecutiveDuration"] = np.mean(consecutive["ConsecutiveDuration"])
                    curDic["speed Mean"] = np.mean(consecutive["totalvelocity"])
                    curDic["MergingDistanceRatio Mean"] = np.mean(consecutive["MergingDistanceRatio"])
                    curDic["MergingDuration Mean"] = np.mean(consecutive["MergingDuration"])
                else:
                    curDic["ConsecutiveDuration"] = 0
                    curDic["speed Mean"] = 0
                    curDic["MergingDistanceRatio Mean"] = 0
                    curDic["MergingDuration Mean"] = 0
                statistc = pd.concat([statistc, pd.DataFrame([curDic])], axis=0)

employColumns = ['DISTANCE', 'location', 'vehicleClass', 'MergingType', 'Count', 'PercentMergingType', 'ConsecutiveDuration']

carStatistc = statistc[(statistc["vehicleClass"] == "car") & (statistc["MergingType"] != "G") & (statistc["MergingType"] != "H")][employColumns]
carStatistc.sort_values(by="MergingType", inplace=True)
carStatistc['MergingType']= carStatistc['MergingType'].astype('category')

statistic =  pd.DataFrame()
for locationId, locationGroup in carStatistc.groupby("location"):
    for mergingType, mergingTypeGroup in locationGroup.groupby("MergingType"):
        average = {}
        average["DISTANCE"] = "average"
        average["location"] = locationId
        average["vehicleClass"] = "car"
        average["MergingType"] = mergingType
        average["Count"] = np.mean(mergingTypeGroup["Count"])
        average["PercentMergingType"] = np.mean(mergingTypeGroup["PercentMergingType"])
        average["ConsecutiveDuration"] = np.mean(mergingTypeGroup["ConsecutiveDuration"])
        current = pd.concat([mergingTypeGroup, pd.DataFrame([average])], axis=0)
        statistic = pd.concat([statistic,current], axis=0)

print(statistic[statistic["DISTANCE"]=="average"])

FONTSIZE = 16
plt.figure(figsize=(24, 10))
plt.style.use('seaborn-colorblind')

i = 1
for distance in [100,150,200,"average"]:
    location2CarStatistc = statistic[( statistic["location"] == 2 ) & ( statistic["DISTANCE"] == distance)]
    location3CarStatistc = statistic[( statistic["location"] == 3 ) & ( statistic["DISTANCE"] == distance)]
    location5CarStatistc = statistic[( statistic["location"] == 5 ) & ( statistic["DISTANCE"] == distance)]
    location6CarStatistc = statistic[( statistic["location"] == 6 ) & ( statistic["DISTANCE"] == distance)]

    ax1 = plt.subplot(2,4,i)
    plt.plot(location2CarStatistc["PercentMergingType"].values,'-',linewidth =2.5, label="locaion2", alpha=0.9)
    plt.plot(location3CarStatistc["PercentMergingType"].values,'--',linewidth =2.5,label="locaion3", alpha=0.9)
    plt.plot(location5CarStatistc["PercentMergingType"].values,'-.',linewidth =2.5,label="locaion5", alpha=0.9)
    plt.plot(location6CarStatistc["PercentMergingType"].values,'o--',linewidth =2.5,label="locaion6", alpha=0.9)
    sns.set_context("notebook")
    plt.grid(ls='--', axis="both")
    plt.style.use('seaborn-colorblind')
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0, 0.1,0.2,0.3,0.4,0.5,0.6,0.7])
    plt.xticks([0,1,2,3,4,5], ["A","B","C","D","E","F"])
    plt.legend(prop=fontlegend)
    plt.ylabel("Percent", font1)
    plt.title("DISTANCE="+str(distance),font1)

    i +=1

for distance in [100,150,200,"average"]:

    ax2 = plt.subplot(2,4,i)
    g1 = sns.barplot(x="MergingType", y="ConsecutiveDuration", hue="location", data=statistic[statistic["DISTANCE"] == distance],palette="hls")
    g1.set(xlabel=None)
    sns.set_context("notebook")
    plt.grid(ls='--', axis="both")
    plt.style.use('seaborn-colorblind')
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.xticks([0,1,2,3,4,5], ["A","B","C","D","E","F"])
    plt.yticks([0,1,2,3,4,5,6,7,8,9,10])
    plt.ylabel("Time(s)", font1)
    plt.title("DISTANCE="+str(distance),font1)
    i +=1

plt.tight_layout()
plt.savefig(root_path+"/asset/consecutiveLaneChange/occurrenceAndDuration.png", dpi=300)
