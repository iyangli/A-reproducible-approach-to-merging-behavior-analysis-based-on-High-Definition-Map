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

FONTSIZE = 16
plt.figure(figsize=(22, 16))
plt.style.use('seaborn-colorblind')

j = 0
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

    mergingData['miniTTC'] = mergingData.loc[:, ['MiniRearTTC', 'MiniLeadTTC']].min(axis=1)

    for curLocation, curLocationGroup in mergingData.groupby("location"):
        for curVehicleClass, curVehicleGroup in curLocationGroup.groupby("vehicleClass"):
            for curMergingType, curMergingTypeGroup in curVehicleGroup.groupby("MergingType"):
                filterData = curMergingTypeGroup[curMergingTypeGroup["miniTTC"]<=15]

                curDic = {}
                curDic["DISTANCE"] = i
                curDic["location"] = curLocation
                curDic["vehicleClass"] = curVehicleClass
                curDic["MergingType"] = curMergingType
                curDic["Count"] = len(filterData)
                curDic["percentage"] = len(filterData)/len(curMergingTypeGroup)

                curDic["miniTTC Mean"] = np.mean(filterData["miniTTC"])

                statistc = pd.concat([statistc, pd.DataFrame([curDic])], axis=0)

statistc.to_excel(root_path+"/asset/table/table_SafetyAnalysis.xlsx")
