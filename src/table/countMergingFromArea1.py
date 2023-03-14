import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

root_path = os.path.abspath('../../')
data_path = root_path+"/asset/mergingData.csv"
ori_data = pd.read_csv(data_path)

employedColumns = ['location', 'vehicleClass',"trackId"]
crossSolidLineTable =  ori_data[(ori_data['MergingState']==True) & (ori_data['RouteClass']=='entry') & (ori_data['BreakRuleState']=='Yes')]
location2Car = ori_data[(ori_data['MergingState']==True) & (ori_data['RouteClass']=='entry')  & (ori_data['location']==2)]
location5Car = ori_data[(ori_data['MergingState']==True) & (ori_data['RouteClass']=='entry')  & (ori_data['location']==5)]
crossSolidLineTable[employedColumns].groupby(["location","vehicleClass"]).describe(include='all').to_csv(root_path+"/asset/table2_countMergingFromArea1.csv")

print(len(location2Car))
print(len(location5Car))
print(crossSolidLineTable.describe())









