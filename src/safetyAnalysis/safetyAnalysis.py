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

oriData100m = pd.read_csv(root_path+"/asset/mergingDataSafety100m.csv")
# oriData150m = pd.read_csv(root_path+"/asset/mergingDataSafety150m.csv")
# oriData200m = pd.read_csv(root_path+"/asset/mergingDataSafety200m.csv")


for curlocationId, curlocationGroup in oriData100m.groupby("location"):
    plt.figure(figsize=(16, 8))
    ax1 = plt.subplot(111)
    plt.style.use('seaborn-colorblind')

    for curRecordingId, curRecordingGroup in curlocationGroup.groupby("recordingId"):
        for curVehicleId, curVehicleGroup in curRecordingGroup.groupby("trackId"):

            if "A" in curVehicleGroup["MergingType"].values :
                plt.scatter(np.arange(0,len(curVehicleGroup)),curVehicleGroup["latLaneCenterOffset"],s=0.2,c="black")
            elif "B" in curVehicleGroup["MergingType"].values :
                plt.scatter(np.arange(0,len(curVehicleGroup)),curVehicleGroup["latLaneCenterOffset"],s=0.2,c="green")
            elif "C" in curVehicleGroup["MergingType"].values :
                plt.scatter(np.arange(0,len(curVehicleGroup)),curVehicleGroup["latLaneCenterOffset"],s=0.2,c="yellow")
            elif "D" in curVehicleGroup["MergingType"].values :
                plt.scatter(np.arange(0,len(curVehicleGroup)),curVehicleGroup["latLaneCenterOffset"],s=0.2,c="blue")
            elif "E" in curVehicleGroup["MergingType"].values :
                plt.scatter(np.arange(0,len(curVehicleGroup)),curVehicleGroup["latLaneCenterOffset"],s=0.2,c="red")
            elif "F" in curVehicleGroup["MergingType"].values :
                plt.scatter(np.arange(0,len(curVehicleGroup)),curVehicleGroup["latLaneCenterOffset"],s=0.2,c="cyan")

    plt.show()

    plt.clf()







