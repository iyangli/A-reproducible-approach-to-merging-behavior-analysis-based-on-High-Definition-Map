import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from util import common
import seaborn as sns
import os

rootPath = os.path.abspath('../../../')
oriData = pd.read_csv(rootPath+"/asset/mergingData100m.csv",low_memory=False)

mergingData = oriData[(oriData['MergingState']==True) & (oriData['RouteClass']=='entry') & (oriData['BreakRuleState']=='None')]
nineRandomMergingData = mergingData.sample(n=8,random_state=3)

WINDOW = 5/0.04
i = 1

plt.figure(figsize=(16, 6.5))
sns.set_style("whitegrid")

number = {"1":"a","2":"b","3":"c","4":"d","5":"e","6":"f","7":"g","8":"h","9":"i"}

for curLocationId,curLocationGroup in nineRandomMergingData.groupby("location"):
    for curRecordingId, curRecordingGroup in curLocationGroup.groupby("recordingId"):
        tracksCsvPath = rootPath+ "/drone-dataset-tools-master/data/" + str(curRecordingId) + "_tracks.csv"
        tracksCsv = pd.read_csv(tracksCsvPath)
        for curVehicleId, curVehicleGroup in curRecordingGroup.groupby("trackId"):
            curVehicleTracks = tracksCsv[tracksCsv["trackId"]==curVehicleId]

            curLcMomentData = curVehicleTracks[curVehicleTracks["laneChange"] == 1]
            effectiveFrame = common.filterLaneChange(curLcMomentData.index.values)

            left = max(min(effectiveFrame)-WINDOW,0)
            right = min(max(effectiveFrame)+WINDOW,max(curVehicleTracks.index.values))

            curVehicleTracks = curVehicleTracks.loc[left:right,:]
            curVehicleTracks["lonVelocityRevised"] = curVehicleTracks.apply(lambda row: common.calculateLonVelocity(row, "lon", "Velocity"),axis=1)
            curVehicleTracks["latVelocityRevised"] = curVehicleTracks.apply(lambda row: common.calculateLonVelocity(row, "lat", "Velocity"),axis=1)
            curVehicleTracks["lonAccelerationRevised"] = curVehicleTracks.apply(lambda row: common.calculateLonVelocity(row, "lon", "Acceleration"), axis=1)
            curVehicleTracks["latAccelerationRevised"] = curVehicleTracks.apply(lambda row: common.calculateLonVelocity(row, "lat", "Acceleration"), axis=1)
            curVehicleTracks["latLaneCenterOffsetNew"] = curVehicleTracks.apply(lambda row: common.processLaneletData(row["latLaneCenterOffset"], "float"), axis=1)

            ax1 = plt.subplot(2,4,i)
            plt.title("location=" + str(curLocationId) + "\nrecording=" + str(curRecordingId) + ",vehicle=" + str(curVehicleId))
            plt.plot(np.arange(0, len(curVehicleTracks)), curVehicleTracks["latLaneCenterOffsetNew"].values)
            plt.xlabel(number[str(i)]+")"+" frame")
            plt.ylabel("latLaneCenterOffset")
            plt.grid(ls='-', axis="both")
            sns.set_context("notebook")
            plt.yticks([-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5])
            plt.grid(linestyle='--')
            i =i + 1


plt.tight_layout()
# plt.show()
plt.savefig(rootPath+"/asset/preliminaryAnalysis/randomNineTrajectory.png", dpi=600)

