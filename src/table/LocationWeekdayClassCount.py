#!python3
__author__ = "Yang Li"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import ticker

# python console show all
pd.set_option('max_colwidth',200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# absolute path
root_path = os.path.abspath('../../')
output_path =  root_path + "/asset/datasetPreprocess/classificationStatistics/"

# Loop each file
locationClassStatistic =pd.DataFrame()
recordingClassCount = pd.DataFrame()
tracksMetaAll=pd.DataFrame()

# duraction
durationDic = {
    "location 0": 0,
    "location 1": 0,
    "location 2": 0,
    "location 3": 0,
    "location 4": 0,
    "location 5": 0,
    "location 6": 0,
}

# startTime
startTimeLocation0 = []
startTimeLocation1 = []
startTimeLocation2 = []
startTimeLocation3 = []
startTimeLocation4 = []
startTimeLocation5 = []
startTimeLocation6 = []

# speedLimit
# speedLimitLocation0 = []
# speedLimitLocation1 = []
# speedLimitLocation2 = []
# speedLimitLocation3 = []
# speedLimitLocation4 = []
# speedLimitLocation5 = []
# speedLimitLocation6 = []



for i in range(0,93):
    # read data
    cur_data_id = "%02d" % i
    cur_path_tracksMeta = root_path + "/drone-dataset-tools-master/data/" + str(cur_data_id) + "_tracksMeta.csv"
    cur_path_recordingMeta = root_path + "/drone-dataset-tools-master/data/" + str(cur_data_id) + "_recordingMeta.csv"
    tracksMeta_data = pd.read_csv(cur_path_tracksMeta)
    recordingMeta_data = pd.read_csv(cur_path_recordingMeta)

    # match location and weekday
    tracksMeta_data["locationId"] = recordingMeta_data["locationId"].values[0]
    tracksMeta_data["weekday"] = recordingMeta_data["weekday"].values[0]
    tempData = tracksMeta_data[["recordingId","trackId","class","locationId","weekday"]]
    locationClassStatistic = pd.concat([locationClassStatistic, tempData], axis=0, ignore_index=True)

    # count by vehicle type for each recording
    currentRecordingClassCount = tracksMeta_data["class"].value_counts().rename_axis('vehicle type').reset_index(name='counts')
    currentRecordingClassCount["recordingID"] = cur_data_id
    recordingClassCount = pd.concat([recordingClassCount,currentRecordingClassCount], axis=0)

    tracksMetaAll = pd.concat([tracksMetaAll, recordingMeta_data], axis=0)


    # duration for each location

    cur_data_id = float(cur_data_id)
    if cur_data_id in list(range(0,19,1)):
        durationDic["location 0"] += recordingMeta_data["duration"].values[0]
    elif cur_data_id in list(range(19,39,1)):
        durationDic["location 1"] += recordingMeta_data["duration"].values[0]
    elif cur_data_id in list(range(39,53,1)):
        durationDic["location 2"] += recordingMeta_data["duration"].values[0]
    elif cur_data_id in list(range(53,61,1)):
        durationDic["location 3"] += recordingMeta_data["duration"].values[0]
    elif cur_data_id in list(range(61,73,1)):
        durationDic["location 4"] += recordingMeta_data["duration"].values[0]
    elif cur_data_id in list(range(73,78,1)):
        durationDic["location 5"] += recordingMeta_data["duration"].values[0]
    else:
        durationDic["location 6"] += recordingMeta_data["duration"].values[0]


    # startTime for each location

    cur_data_id = float(cur_data_id)
    if cur_data_id in list(range(0,19,1)):
        startTimeLocation0.append(recordingMeta_data["startTime"].values[0])
    elif cur_data_id in list(range(19,39,1)):
        startTimeLocation1.append(recordingMeta_data["startTime"].values[0])
    elif cur_data_id in list(range(39,53,1)):
        startTimeLocation2.append(recordingMeta_data["startTime"].values[0])
    elif cur_data_id in list(range(53,61,1)):
        startTimeLocation3.append(recordingMeta_data["startTime"].values[0])
    elif cur_data_id in list(range(61,73,1)):
        startTimeLocation4.append(recordingMeta_data["startTime"].values[0])
    elif cur_data_id in list(range(73,78,1)):
        startTimeLocation5.append(recordingMeta_data["startTime"].values[0])
    else:
        startTimeLocation6.append(recordingMeta_data["startTime"].values[0])

print(tracksMetaAll)

print('-------------')
currentTracksMetaAll=pd.DataFrame
for cur_group_id, cur_group_data in tracksMetaAll.groupby("locationId"):
    for cur_group_id2, cur_group_data2 in cur_group_data.groupby("startTime"):
        print(str(cur_group_id)+','+str(cur_group_id2)+','+str(sum(cur_group_data2['numTracks']))+','+str(sum(cur_group_data2['duration'])))


tracksMetaAll = pd.DataFrame()

print('startTime for every location:')
print(startTimeLocation0)
print(startTimeLocation1)
print(startTimeLocation2)
print(startTimeLocation3)
print(startTimeLocation4)
print(startTimeLocation5)
print(startTimeLocation6)


# class\weekday for each location
class_count = pd.DataFrame()
weekday_count = pd.DataFrame()

for cur_group_id, cur_group_data in locationClassStatistic.groupby("locationId"):
    cur_group_data = cur_group_data[["class","locationId","weekday"]]
    cur_class_group =  cur_group_data.groupby('class').count()
    cur_class_group['loc']= cur_group_id
    cur_weekday_group =  cur_group_data.groupby('weekday').count()
    cur_weekday_group['loc'] = cur_group_id
    class_count = pd.concat([class_count,cur_class_group ], axis=0)
    weekday_count = pd.concat([weekday_count,cur_weekday_group], axis=0)
class_count = class_count .reset_index()
weekday_count = weekday_count .reset_index()[['loc','weekday']]
class_count.to_csv(output_path+"/table/locationClassCount.csv")
weekday_count.to_csv(output_path+"/table/locationWeekdayCount.csv")

# #-------------------------------------------------------------------------------------------------------
# # VehicleClass for every location
# colors=('#f1d9c3','#b3cdd6','#edbab7')

def vehicle_class():
    colors=('#d5cec4','#c9d0d8','#f1f3eb')

    Car = class_count[class_count['class']=="car"]["locationId"].values
    Truck= class_count[class_count['class']=="truck"]["locationId"].values
    Van= class_count[class_count['class']=="van"]["locationId"].values
    Sum = Car + Truck + Van

    fig = plt.figure(figsize=(8,4.5))

    X=['0','1', '2', '3', '4', '5', '6']
    ax1 = plt.subplot(111)
    data=pd.DataFrame({'Car':Car, 'Truck':Truck,'Van':Van})
    data.plot(kind='bar', stacked=True,color=colors,edgecolor='black',ax=ax1)
    plt.legend(loc=2)
    plt.ylabel('Number of vehicles',fontproperties = 'Times New Roman',size=14)
    plt.yticks(np.arange(0, 16010, 2000),fontproperties = 'Times New Roman',size=12)
    plt.xticks (range(0,7,1),X,rotation=0,fontproperties = 'Times New Roman',size=12)

    ax2 = ax1.twinx()
    Y2=durationDic.values()

    totalTime = sum(Y2)
    mew = [x/totalTime for x in Y2 ]

    plt.plot(X,[x/totalTime for x in Y2],color='#89231d',alpha=0.9,linestyle='--',linewidth=2,marker='D',label='Recording duration proportion')
    plt.yticks(np.arange(0, 0.30, 0.05),fontproperties = 'Times New Roman',size=12)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xlabel('LocationID',fontproperties = 'Times New Roman',size=14)
    ax2.set_ylabel('Rel.Recording duration proportion(%)',fontproperties = 'Times New Roman',size=14)
    ax1.grid(axis='y', linestyle='--')
    plt.show()
    # plt.savefig(output_path+"/picture/locationVehicleClass.png", dpi=600)

vehicle_class()

#-------------------------------------------------------------------------------------------------------
# truck proportion
def vehicle_class2():

    colors=('#d5cec4','#c9d0d8','#f1f3eb')

    Car = class_count[class_count['class']=="car"]["locationId"].values
    Truck= class_count[class_count['class']=="truck"]["locationId"].values
    Van= class_count[class_count['class']=="van"]["locationId"].values
    Sum = Car + Truck + Van

    fig = plt.figure(figsize=(8,4.5))

    X=['0','1', '2', '3', '4', '5', '6']
    ax1 = plt.subplot(111)
    data=pd.DataFrame({'Car':Car, 'Truck':Truck,'Van':Van})
    data.plot(kind='bar', stacked=True,color=colors,edgecolor='black',linewidth=1.25,ax=ax1,zorder=100)
    plt.legend(loc=2)
    plt.ylabel('Number of vehicles',fontproperties = 'Times New Roman',size=14)
    plt.yticks(np.arange(0, 16010, 2000),fontproperties = 'Times New Roman',size=12)
    plt.xticks (range(0,7,1),X,rotation=0,fontproperties = 'Times New Roman',size=12)
    plt.grid(axis='y', linestyle='--',zorder=-1)

    ax2 = ax1.twinx()
    plt.plot(X,Truck/Sum,color='#89231d',alpha=0.9,linestyle='--',linewidth=1.5,marker='D',label='Recording truck proportion')
    plt.yticks(np.arange(0, 0.40, 0.05),fontproperties = 'Times New Roman',size=12)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xlabel('LocationID',fontproperties = 'Times New Roman',size=14)
    ax2.set_ylabel('Truck proportion(%)',fontproperties = 'Times New Roman',size=14)

    # plt.show()
    plt.savefig(output_path+"/picture/locationVehicleClass2.png", dpi=600)

vehicle_class2()

#-------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------
# roadtype
def roadtype():
    colors=('#C1B8C8','#A9DDD6','#91ADC2')
    fig = plt.figure(figsize=(8, 4.5))

    dpath=  root_path + "/asset/datasetPreprocess/classificationStatistics/table/roadTypeClassCount.csv"
    roadTypeClassCount=pd.read_csv(dpath)

    locationRoadtype =pd.DataFrame()
    roadTypeClassCount_group=roadTypeClassCount.groupby('location')
    print(roadTypeClassCount_group)
    for cur_id, cur_group in roadTypeClassCount_group:
        cur ={}
        cur["location"] = cur_id
        cur["onramp"] = len(cur_group[cur_group["roadtype"]=="onramp"])
        cur["offramp"] = len(cur_group[cur_group["roadtype"]=="offramp"])
        cur["mainline"] = len(cur_group[cur_group["roadtype"]=="mainline"])
        locationRoadtype = pd.concat([locationRoadtype, pd.DataFrame([cur])], axis=0, ignore_index=True)

    Onramp = locationRoadtype["onramp"].values
    Offramp = locationRoadtype["offramp"].values
    Mainline = locationRoadtype["mainline"].values
    Sum2 = Onramp + Offramp + Mainline

    ax1 = plt.subplot(111)
    x=np.arange(7)
    data=pd.DataFrame({'Onramp':Onramp, 'offramp':Offramp,'mainline':Mainline})
    print(data)
    data.plot(kind='bar', stacked=True,color=colors,edgecolor='black',linewidth=1.25,ax=ax1,alpha=0.8,zorder=100)

    plt.legend(loc=2)
    plt.ylabel('Number of vehicles',fontproperties = 'Times New Roman',size=14)
    plt.xlabel('LocationID',fontproperties = 'Times New Roman',size=14)
    plt.yticks(np.arange(0, 16010, 2000),fontproperties = 'Times New Roman',size=12)
    plt.xticks (range(0,7,1),x,rotation=0,fontproperties = 'Times New Roman',size=12)
    plt.grid(axis='y', linestyle='--',zorder=1)


    ax2 = ax1.twinx()
    plt.plot(x,Onramp/Sum2,color='#2d435f',alpha=0.9,linestyle='--',linewidth=1.5,marker='D',label='Recording Onramp proportion')
    plt.yticks(np.arange(0, 0.40, 0.05),fontproperties = 'Times New Roman',size=12)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xlabel('LocationID',fontproperties = 'Times New Roman',size=14)
    ax2.set_ylabel('Onramp proportion(%)',fontproperties = 'Times New Roman',size=14)

    # plt.show()
    plt.savefig(output_path+"/picture/locationRoadtype.png", dpi=600)

roadtype()

#------------------------------------------------------------------------------------------------------
# VehicleClass for every recording
def VehicleClass_for_every_recording():
    Car = recordingClassCount[recordingClassCount['vehicle type']=="car"]["counts"].values
    Truck= recordingClassCount[recordingClassCount['vehicle type']=="truck"]["counts"].values
    Van= recordingClassCount[recordingClassCount['vehicle type']=="van"]["counts"].values
    total = Car + Truck + Van

    fig = plt.figure(figsize=(8,4.5))
    df=pd.DataFrame({'Car':Car, 'Truck':Truck,'Van':Van})
    colors=('#f1d9c3','#b3cdd6','#edbab7')
    df.plot(kind='bar', stacked=True,color=colors,edgecolor='black')
    plt.ylabel('Number of vehicles',fontproperties = 'Times New Roman',size=14)
    plt.xlabel('RecordingID',fontproperties = 'Times New Roman',size=14)
    plt.xticks (range(0,93,10),rotation=0,fontproperties = 'Times New Roman',size=12)
    plt.yticks(np.arange(0, 5000, 500),fontproperties = 'Times New Roman',size=12)

    plt.legend()
    plt.grid(axis='y',ls='--')
    plt.show()
    plt.savefig(output_path+"/picture/recordingVehicleClass.png", dpi=600)
VehicleClass_for_every_recording()
# VehicleClass_for_every_recording()

#-----------------------------------------------------------------------------------------------------------------------
# location Roadtype 并列柱状图
def Side_by_side_bar_chart_for_road_type():
    dpath=  root_path + "/asset/datasetPreprocess/classificationStatistics/table/roadTypeClassCount.csv"
    roadTypeClassCount=pd.read_csv(dpath)
    fig = plt.figure(figsize=(8,4.5))

    locationRoadtype =pd.DataFrame()
    roadTypeClassCount_group=roadTypeClassCount.groupby('location')
    print(roadTypeClassCount_group)
    for cur_id, cur_group in roadTypeClassCount_group:
        print(cur_group.groupby("roadtype").count())
        cur ={}
        cur["location"] = cur_id
        cur["onramp"] = len(cur_group[cur_group["roadtype"]=="onramp"])
        cur["offramp"] = len(cur_group[cur_group["roadtype"]=="offramp"])
        cur["mainline"] = len(cur_group[cur_group["roadtype"]=="mainline"])
        locationRoadtype = pd.concat([locationRoadtype, pd.DataFrame([cur])], axis=0, ignore_index=True)

    bar_width = 0.2

    x=np.arange(7)
    tick_label = ['0', '1', '2', "3","4", "5", "6"]
    plt.bar(x, locationRoadtype['onramp'], bar_width, align="center", color="#A9DDD6", label="onramp",alpha=0.9,edgecolor = 'black')
    plt.bar(x + bar_width, locationRoadtype['offramp'], bar_width, color="#91ADC2", align="center", label="offramp", alpha=0.9,edgecolor = 'black')
    plt.bar(x + 2 * bar_width, locationRoadtype['mainline'], bar_width, color="#C1B8C8", align="center", label="mainline", alpha=0.9,edgecolor = 'black')
    plt.xlabel("LocationID",size=14,fontproperties = 'Times New Roman')
    plt.ylabel("Number of vehicles",size=14,fontproperties = 'Times New Roman')
    plt.xticks(x + bar_width / 2, tick_label,fontproperties = 'Times New Roman',size=12)
    plt.yticks(np.arange(0, 15000, 2000),fontproperties = 'Times New Roman',size=12)
    plt.legend()
    plt.grid(axis='y',ls='--')
    plt.show()
    plt.savefig(output_path+"/picture/locationRoadtype.png", dpi=600)

Side_by_side_bar_chart_for_road_type()

#-----------------------------------------------------------------------------------------------------------------------
