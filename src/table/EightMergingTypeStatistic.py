import pandas as pd
import os
import warnings
import numpy as np
warnings.filterwarnings('ignore')

root_path = os.path.abspath('../../')

statistc = pd.DataFrame()

for i in [100,150,200]:
    data_path = root_path + "/asset/mergingData" + str(i) + "m.csv"
    ori_data = pd.read_csv(data_path)

    mergingData = ori_data[
        (ori_data['MergingState']==True)
        & (ori_data['RouteClass']=='entry')
        & (ori_data['BreakRuleState']=='None')
        & (ori_data['MergingDistance'] !='None')
        & (ori_data['MaxLateralSpeed'] !='None')]

    mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
    mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
    mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
    mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
    mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
    mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))

    employedColumns = ['totalvelocity',  'location', 'vehicleClass', 'MergingDistance', 'MergingDistanceRatio','MergingDuration',"MaxLateralSpeed","MaxiLateralAcc","MinimumRearStatus","MinimumLeadStatus"]

    for curLocation, curLocationGroup in mergingData.groupby("location"):
        for curVehicleClass, curVehicleGroup in curLocationGroup.groupby("vehicleClass"):
            for curMergingType, curMergingTypeGroup in curVehicleGroup.groupby("MergingType"):

                curDic = {}
                curDic["DISTANCE"] = i
                curDic["location"] = curLocation
                curDic["vehicleClass"] = curVehicleClass
                curDic["type"] = curMergingType
                curDic["count"] = len(curMergingTypeGroup)
                curDic["speed Mean"] = np.mean(curMergingTypeGroup["totalvelocity"])
                curDic["MergingDistanceRatio Mean"] = np.mean(curMergingTypeGroup["MergingDistanceRatio"])
                curDic["MergingDuration Mean"] = np.mean(curMergingTypeGroup["MergingDuration"])
                curDic["MaxLateralSpeed Mean"] = np.mean(curMergingTypeGroup["MaxLateralSpeed"])
                curDic["MaxiLateralAcc Mean"] = np.mean(curMergingTypeGroup["MaxiLateralAcc"])

                statistc = pd.concat([statistc, pd.DataFrame([curDic])], axis=0)

statistc.to_excel(root_path+"/asset/table/EightMergingTypeStatistic.xlsx")





