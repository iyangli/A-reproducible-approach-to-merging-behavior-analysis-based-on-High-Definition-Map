import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
import scipy.stats as st

root_path = os.path.abspath('../../')
data_path = root_path+"/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[(ori_data['MergingState']==True) & (ori_data['RouteClass']=='entry') & (ori_data['BreakRuleState']=='None') & (ori_data['MergingDistance'] !='None')  & (ori_data['MaxLateralSpeed'] !='None') ]
mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))

employedColumns = ['totalvelocity',  'location', 'vehicleClass', 'MergingDistance', 'MergingDistanceRatio','MergingDuration',"MaxLateralSpeed","MaxiLateralAcc"]

statistc= pd.DataFrame()
for curLocation, curLocationGroup in mergingData.groupby("location"):
    for curVehicleClass, curVehicleGroup in curLocationGroup.groupby("vehicleClass"):
        curDic = {}
        curDic["location"] = curLocation
        curDic["vehicleClass"] = curVehicleClass

        curDic["speed Mean"] = np.mean(curVehicleGroup["totalvelocity"])
        curDic["speed Std"] = np.std(curVehicleGroup["totalvelocity"])
        curDic["speed ExtremeDeviation"] = np.max(curVehicleGroup["totalvelocity"])-np.min(curVehicleGroup["totalvelocity"])
        curDic["speed Skew"] = st.skew(curVehicleGroup["totalvelocity"])
        curDic["speed Kurtosis"] = st.kurtosis(curVehicleGroup["totalvelocity"])

        curDic["MergingDistanceRatio Mean"] = np.mean(curVehicleGroup["MergingDistanceRatio"])
        curDic["MergingDistanceRatio Std"] = np.std(curVehicleGroup["MergingDistanceRatio"])
        curDic["MergingDistanceRatio ExtremeDeviation"] = np.max(curVehicleGroup["MergingDistanceRatio"])-np.min(curVehicleGroup["MergingDistanceRatio"])
        curDic["MergingDistanceRatio Skew"] = st.skew(curVehicleGroup["MergingDistanceRatio"])
        curDic["MergingDistanceRatio Kurtosis"] = st.kurtosis(curVehicleGroup["MergingDistanceRatio"])

        curDic["MergingDuration Mean"] = np.mean(curVehicleGroup["MergingDuration"])
        curDic["MergingDuration Std"] = np.std(curVehicleGroup["MergingDuration"])
        curDic["MergingDuration ExtremeDeviation"] = np.max(curVehicleGroup["MergingDuration"])-np.min(curVehicleGroup["MergingDuration"])
        curDic["MergingDuration Skew"] = st.skew(curVehicleGroup["MergingDuration"])
        curDic["MergingDuration Kurtosis"] = st.kurtosis(curVehicleGroup["MergingDuration"])

        curDic["MaxLateralSpeed Mean"] = np.mean(curVehicleGroup["MaxLateralSpeed"])
        curDic["MaxLateralSpeed Std"] = np.std(curVehicleGroup["MaxLateralSpeed"])
        curDic["MaxLateralSpeed ExtremeDeviation"] = np.max(curVehicleGroup["MaxLateralSpeed"])-np.min(curVehicleGroup["MaxLateralSpeed"])
        curDic["MaxLateralSpeed Skew"] = st.skew(curVehicleGroup["MaxLateralSpeed"])
        curDic["MaxLateralSpeed Kurtosis"] = st.kurtosis(curVehicleGroup["MaxLateralSpeed"])

        curDic["MaxiLateralAcc Mean"] = np.mean(curVehicleGroup["MaxiLateralAcc"])
        curDic["MaxiLateralAcc Std"] = np.std(curVehicleGroup["MaxiLateralAcc"])
        curDic["MaxiLateralAcc ExtremeDeviation"] = np.max(curVehicleGroup["MaxiLateralAcc"])-np.min(curVehicleGroup["MaxiLateralAcc"])
        curDic["MaxiLateralAcc Skew"] = st.skew(curVehicleGroup["MaxiLateralAcc"])
        curDic["MaxiLateralAcc Kurtosis"] = st.kurtosis(curVehicleGroup["MaxiLateralAcc"])

        statistc = pd.concat([statistc, pd.DataFrame([curDic])], axis=0)

statistc.set_index(["location","vehicleClass"],inplace=True)
statistc.to_csv(root_path+"/asset/statisticMergingDistanceDurationSpeed.csv")


