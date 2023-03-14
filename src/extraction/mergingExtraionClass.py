import os
import numpy as np
import pandas as pd
from loguru import logger
import warnings
from conf import laneletID
from util import common
warnings.filterwarnings("ignore")

class MergingExtracionClass(object):
    def __init__(self,config):
        self.config = config
        self.TIMESTEP = config["timestep"]
        self.DISTANCE = config["distance_threshold"]
        self.LOOKBACK = config["lookback"]

        self.rootPath = os.path.abspath('../../')
        self.savePath = os.path.abspath('../../') + "/asset/"
        self.outputPath = self.savePath + "mergingData"+str(self.DISTANCE)+"m.csv"

        self.usedColumns = ['recordingId', 'trackId', 'frame', 'trackLifetime', 'xCenter', 'yCenter', 'heading',
                            'xVelocity', 'yVelocity', 'xAcceleration', 'yAcceleration', 'lonVelocity', 'latVelocity',
                            'lonAcceleration', 'latAcceleration', 'traveledDistance', 'latLaneCenterOffset',
                            'laneletId', 'laneChange', 'lonLaneletPos', 'leadId', 'rearId', 'leftLeadId', 'leftRearId',
                            'leftAlongsideId', 'curxglobalutm', 'curyglobalutm']

        self.location = None
        self.HDMdata = None
        self.tracksBeforeMerge = None
        self.tracksSelf = None
        self.trackselftail = None
        self.tailLeadVehicles = None
        self.tailRearVehicles = None
        self.tracksSelfInArea23 = None
        self.tracksSelfInArea123 = None
        self.tracksSelfInArea4 = None
        self.tracksSelfInArea5 = None
        self.tracksOtherInTimeArea123 = None
        self.leftIndex = None
        self.rightIndex = None
        self.alongsidetolead = None
        self.alongsidetorear = None
        self.reartofront = None
        self.leftalongsidevehicles = None
        self.leadvehicles = None
        self.leftleadvehicles = None
        self.rearvehicles = None
        self.leftRearvehicles = None
        self.metricAreaUpstream = "area4"
        self.metricAreaWeaving = "area5"

        self.surroundingVehiclesLabel = ["leadId",
                                         "rearId",
                                         "leftLeadId",
                                         "leftRearId",
                                         "leftAlongsideId",
                                         "rightLeadId",
                                         "rightRearId",
                                         "rightAlongsideId"]

        self.safetyAnalysisData = None
        self.TTCThreshold = 2
        self.outputPathSafety = self.savePath + "mergingDataSafety"+str(self.DISTANCE)+"m.csv"

        self.locationTotalMergingDistance = {
            "2": 160.32,
            "3": 200.52,
            "5": 174.81,
            "6": 219.72
        }

        self.recordingMapToLocation = {
            "0": list(range(0, 19)),
            "1": list(range(19, 39)),
            "2": list(range(39, 53)),
            "3": list(range(53, 61)),
            "4": list(range(61, 73)),
            "5": list(range(73, 78)),
            "6": list(range(78, 93)),
        }

    def initTracks(self, tracks, row):
        self.tracksBeforeMerge = tracks[tracks["frame"] <= row["frame"]]
        self.tracksSelf = self.tracksBeforeMerge[self.tracksBeforeMerge["trackId"] == row["trackId"]]

        try:
            self.tracksSelfInArea23 = self.tracksSelf[self.tracksSelf["laneletId"].isin(self.HDMdata["area23"])]
            self.tracksSelfInArea123 = self.tracksSelf[self.tracksSelf["laneletId"].isin(self.HDMdata["area123"])]
            self.tracksSelfInArea4 = self.tracksSelf[self.tracksSelf["laneletId"].isin(self.HDMdata["area4"])]
            self.tracksSelfInArea5 = self.tracksSelf[self.tracksSelf["laneletId"].isin(self.HDMdata["area5"])]

            self.tracksOtherInTimeArea123 = self.tracksBeforeMerge[
                (self.tracksBeforeMerge["frame"] >= min(self.tracksSelfInArea123.index.values)) &
                (self.tracksBeforeMerge["frame"] <= max(self.tracksSelfInArea123.index.values))
                ]

            self.tracksSelfInArea123.sort_index(inplace=True)
            self.tracksSelfInArea23.sort_index(inplace=True)
            self.tracksBeforeMerge.sort_index(inplace=True)

            self.trackselftail = tracks[(tracks["frame"] <= (row["frame"]+5)) & (tracks["trackId"] <= (row["trackId"]))].tail(10)
            self.tailLeadVehicles = np.unique(np.concatenate(
                (self.trackselftail["leadId"].values, self.trackselftail["leftLeadId"].values, self.trackselftail["rightLeadId"].values),
                axis=0))
            self.tailRearVehicles = np.unique(np.concatenate(
                (self.trackselftail["rearId"].values, self.trackselftail["leftRearId"].values, self.trackselftail["rightRearId"].values),
                axis=0))

            tmp = self.tracksSelfInArea123
            tmp = tmp.astype({"latLaneCenterOffset": float})
            tmp["leftAlongsideId"] = tmp.apply(
                lambda row: common.processLaneletData(row["leftAlongsideId"], "int"), axis=1)

            tmp["leadId"] = tmp.apply(lambda row: common.processLaneletData(row["leadId"], "int"),
                                      axis=1)
            tmp["leftLeadId"] = tmp.apply(
                lambda row: common.processLaneletData(row["leftLeadId"], "int"), axis=1)
            tmp["rearId"] = tmp.apply(lambda row: common.processLaneletData(row["rearId"], "int"),
                                      axis=1)
            tmp["leftRearId"] = tmp.apply(
                lambda row: common.processLaneletData(row["leftRearId"], "int"), axis=1)

            self.leftalongsidevehicles = tmp["leftAlongsideId"].values
            self.leadvehicles = tmp["leadId"].values
            self.leftleadvehicles = tmp["leftLeadId"].values
            self.rearvehicles = tmp["rearId"].values
            self.leftRearvehicles = tmp["leftRearId"].values

            self.alongsidetolead = list(set(self.leftalongsidevehicles) & set(self.leadvehicles)) \
                                   + list(set(self.leftalongsidevehicles) & set(self.leftleadvehicles))
            self.alongsidetorear = list(set(self.leftalongsidevehicles) & set(self.rearvehicles)) \
                                   + list(set(self.leftalongsidevehicles) & set(self.leftRearvehicles))
            self.reartofront = list(set(self.rearvehicles) & set(self.leadvehicles)) \
                               + list(set(self.rearvehicles) & set(self.leftleadvehicles)) \
                               + list(set(self.leftRearvehicles) & set(self.leadvehicles)) \
                               + list(set(self.leftRearvehicles) & set(self.leftleadvehicles))

            logger.info("Current recording {}, vehicle {} merging, current frame {}", row["recordingId"],
                        row["trackId"], row["frame"])

            return True

        except:
            logger.info("error happen, vehicle {}, frame {}", row["trackId"], row["frame"])

            return False

    def run(self):
        data = pd.DataFrame()

        for record in range(0, 93):

            if record in self.recordingMapToLocation["0"] \
                    or record in self.recordingMapToLocation["1"] \
                    or record in self.recordingMapToLocation["4"]:
                continue

            tracks, tracksmeta, recordingmeta = self.readCSVFile("%02d" % record)
            location = str(recordingmeta["locationId"].values[0])
            weekday = recordingmeta["weekday"].values[0]
            self.HDMdata = laneletID.lanlet2data[location]
            self.location = location
            self.weekday = weekday

            tracks["latLaneCenterOffset"] = tracks.apply(
                lambda row: common.processLaneletData(row["latLaneCenterOffset"], "float"), axis=1)
            
            tracks["laneletId"] = tracks.apply(lambda row: common.processLaneletData(row["laneletId"], "int"),axis=1)
            
            tracks.set_index(keys="frame", inplace=True, drop=False)

            for curid, curgroup in tracks[self.usedColumns].groupby("trackId"):

                if (curgroup["laneChange"].unique() == 0).all() or len(curgroup) < 3 / self.TIMESTEP:
                    continue

                curgroup.sort_index(inplace=True)

                laneChangeMoment = curgroup[curgroup["laneChange"] == 1]
                tmpconcat = laneChangeMoment.loc[common.filterLaneChange(laneChangeMoment.index.values)]

                tmpconcat["location"] = self.location
                tmpconcat["weekday"] = self.weekday
                tmpconcat["vehicleClass"] = tracksmeta[tracksmeta["trackId"] == curid]["class"].values[0]
                tmpconcat["RouteClass"] = self.checkVehicleRouteClass(curgroup)

                tmpconcat["MergingState"] = tmpconcat.apply(
                    lambda row: self.checkMergingStatus(row, tracks, curgroup), axis=1)

                tmpconcat[
                    ["MergingDistance", "MergingDistanceRatio",
                     "BreakRuleState", "BreakRuleArea"]
                ] = tmpconcat.apply(
                    lambda row: self.getMergingDistance(row), axis=1, result_type="expand")

                tmpconcat["MergingDuration"] = tmpconcat.apply(lambda row: self.getMergingDuration(row), axis=1)

                tmpconcat[
                    ["MaxLateralSpeed", "MaxiLateralAcc", "MiniLateralAcc"]
                ] = tmpconcat.apply(lambda row: self.getLateralSpeedandAcceleration(row), axis=1, result_type="expand")

                tmpconcat[
                    ["SurroundingVehiclesInfo", "RearVehicleNumber","MinimumRearDistance",
                     "MinimumRearStatus","MinimumRearClass","LeadVehicleNumber",
                     "MinimumLeadDistance", "MinimumLeadStatus","MinimumLeadClass",
                     "MergingType","LeadVehicleId", "RearVehicleId",
                     "MinimumRearSpeed","MinimumRearHeadway","MinimumLeadSpeed","MinimumLeadHeadway"
                     ]
                ] = tmpconcat.apply(lambda row: self.matchSurroundingVehicles(row, tracksmeta), axis=1, result_type="expand")

                tmpconcat[
                    ["trafficFlowArea4", "trafficDensityArea4",
                     "trafficSpeedArea4", "trafficFlowArea5",
                     "trafficDensityArea5", "trafficSpeedArea5"]
                ] = tmpconcat.apply(lambda row: self.getTrafficFlowDenstiySpeed(row), axis=1, result_type="expand")

                tmpconcat[["LaneChangingCounts", "ConsecutiveDuration"]] = self.calculateConsecutiveLanechange(
                    common.filterLaneChange(tmpconcat.index.values),
                    tmpconcat
                )

                tmpconcat[
                    ["conflictData", "MiniLeadTTC","MiniRearTTC"]
                ] = tmpconcat.apply(
                    lambda row: self.getMinimumTTCRearAndLead(row), axis=1, result_type="expand")

                data = pd.concat([data, tmpconcat[tmpconcat["MergingState"]==True]], axis=0)

            del tracks, tracksmeta, recordingmeta

        data.to_csv(self.outputPath)
        self.safetyAnalysisData.to_csv(self.outputPathSafety)

    def getTTCList(self, surroundingtracksData):
        framelist, TTClist, distancelist, speeddiff = [], [], [], []

        for index, row in self.tracksSelfInArea23.iterrows():
            tmp = surroundingtracksData[surroundingtracksData["frame"] == row["frame"]]
            if tmp.empty:
                continue

            positionself = np.array([row["xCenter"], row["yCenter"]])
            positionother = np.array([tmp["xCenter"].values[0], tmp["yCenter"].values[0]])

            speedself = np.array([row["xVelocity"], row["yVelocity"]])
            speedother = np.array([tmp["xVelocity"].values[0], tmp["yVelocity"].values[0]])

            distance = np.sqrt(np.dot((positionself - positionother), (positionself - positionother).T))
            distance_ = np.dot((positionself - positionother).T, (speedself - speedother)) / distance

            TTC = - distance / distance_

            if TTC < 0 or distance > 50:
                continue

            TTClist.append(TTC)
            distancelist.append(distance)
            speeddiff.append(np.sqrt(np.dot((speedself - speedother), (speedself - speedother).T)))
            framelist.append(row["frame"])

        dic = {
            "frame": framelist,
            "TTC": TTClist,
            "distance": distancelist,
            "relspe": speeddiff,
        }

        if len(TTClist) == 0:
            return 0

        return dic

    def calculateSafetyIndicatros(self,row1,row2):
        leadVehicleId = row1["LeadVehicleId"]
        rearVehicleId = row1["RearVehicleId"]

        curFrame = row2["frame"]
        leadData = self.tracksBeforeMerge[
            (self.tracksBeforeMerge["frame"] == curFrame)
            & (self.tracksBeforeMerge["trackId"] == leadVehicleId)
            ]
        rearData = self.tracksBeforeMerge[
            (self.tracksBeforeMerge["frame"] == curFrame)
            & (self.tracksBeforeMerge["trackId"] == rearVehicleId)
            ]

        positionSelfVector = np.array([row1["xCenter"], row1["yCenter"]])
        speedSelfVector = np.array([abs(row1["xVelocity"]), abs(row1["yVelocity"])])
        speedSelf = np.sqrt(row1["xVelocity"]**2+row1["yVelocity"]**2)

        if  leadData.empty:
            LeadxCenter = "None"
            LeadyCenter = "None"
            LeadxVelocity = "None"
            LeadyVelocity = "None"
            LeadDistance = "None"
            LeadHeadway = "None"
            LeadTTC = "None"
            LeadSpeed = "None"
            DeltaLeadSpeed = "None"
            LeadTTCMinusThreshold = "None"
        else:
            positionLead = np.array([leadData["xCenter"].values[0], leadData["yCenter"].values[0]])
            speedLead = np.array([abs(leadData["xVelocity"].values[0]), abs(leadData["yVelocity"].values[0])])
            distanceLead = np.sqrt(np.dot((positionSelfVector - positionLead), (positionSelfVector - positionLead).T))
            distanceLead_ = np.dot((positionSelfVector - positionLead).T, (speedSelfVector - speedLead)) / distanceLead
            TTCLead = - distanceLead / distanceLead_
            LeadxCenter = leadData["xCenter"].values[0]
            LeadyCenter = leadData["yCenter"].values[0]
            LeadxVelocity = leadData["xVelocity"].values[0]
            LeadyVelocity = leadData["yVelocity"].values[0]
            LeadSpeed = np.sqrt(LeadxVelocity**2+LeadyVelocity**2)
            DeltaLeadSpeed = speedSelf - LeadSpeed
            LeadDistance = distanceLead
            LeadHeadway = distanceLead/ speedSelf
            LeadTTC = TTCLead

            if 0 < LeadTTC <= self.TTCThreshold:
                LeadTTCMinusThreshold = (self.TTCThreshold - LeadTTC) * self.TIMESTEP
            else:
                LeadTTCMinusThreshold = "None"

        if  rearData.empty:
            RearxCenter = "None"
            RearyCenter = "None"
            RearxVelocity = "None"
            RearyVelocity = "None"
            RearDistance = "None"
            RearHeadway = "None"
            RearTTC = "None"
            RearSpeed = "None"
            DeltaRearSpeed = "None"
            RearTTCMinusThreshold = "None"

        else:
            positionRear = np.array([rearData["xCenter"].values[0], rearData["yCenter"].values[0]])
            speedRear = np.array([abs(rearData["xVelocity"].values[0]), abs(rearData["yVelocity"].values[0])])
            distanceRear = np.sqrt(np.dot((positionSelfVector - positionRear), (positionSelfVector - positionRear).T))
            distanceRear_ = np.dot((positionSelfVector - positionRear).T, (speedSelfVector - speedRear)) / distanceRear
            TTCRear = - distanceRear / distanceRear_
            RearxCenter = rearData["xCenter"].values[0]
            RearyCenter = rearData["yCenter"].values[0]
            RearxVelocity = rearData["xVelocity"].values[0]
            RearyVelocity = rearData["yVelocity"].values[0]
            RearSpeed = np.sqrt(RearxVelocity**2+RearyVelocity**2)
            DeltaRearSpeed = speedSelf - RearSpeed
            RearDistance = distanceRear
            RearHeadway = distanceRear/ RearSpeed
            RearTTC = TTCRear

            if 0 < RearTTC <= self.TTCThreshold:
                RearTTCMinusThreshold = (self.TTCThreshold - RearTTC) * self.TIMESTEP
            else:
                RearTTCMinusThreshold = "None"

        if leadData.empty or rearData.empty:
            AcceptedGap = 999
        else:
            AcceptedGap = np.sqrt(
                (leadData["xCenter"].values[0]-rearData["xCenter"].values[0])**2+
                (leadData["yCenter"].values[0]-rearData["yCenter"].values[0])**2
            )

        return RearxCenter, RearyCenter, RearxVelocity, RearyVelocity, \
               LeadxCenter, LeadyCenter, LeadxVelocity, LeadyVelocity, \
               LeadDistance, LeadHeadway, LeadSpeed,DeltaLeadSpeed, LeadTTC,LeadTTCMinusThreshold, \
               RearDistance, RearHeadway, RearSpeed, DeltaRearSpeed, RearTTC,RearTTCMinusThreshold,\
               AcceptedGap,speedSelf

    def outputSafetyData(self,row1):
        columns = [
            'location', 'weekday', 'vehicleClass', 'RouteClass',
            'MergingState', 'MergingDistance', 'MergingDistanceRatio',
            'MergingDuration','MaxLateralSpeed', 'MaxiLateralAcc','MiniLateralAcc',
            'MinimumRearClass', 'MinimumLeadClass',"LeadVehicleId", "RearVehicleId",
            "LaneChangingCounts", "ConsecutiveDuration",
            "trafficFlowArea4", "trafficDensityArea4","trafficSpeedArea4",
            "trafficFlowArea5","trafficDensityArea5", "trafficSpeedArea5",
            'MergingType'
        ]

        curData = self.tracksSelfInArea23
        curData[columns] = row1[columns]
        # print(curData)
        # print(row1)

        curData[
            [
                "RearxCenter", "RearyCenter", "RearxVelocity", "RearyVelocity",
                "LeadxCenter", "LeadyCenter", "LeadxVelocity", "LeadyVelocity",
                "LeadDistance", "LeadHeadway","LeadSpeed","DeltaLeadSpeed", "LeadTTC","LeadTTCMinusThreshold",
                "RearDistance", "RearHeadway","RearSpeed", "DeltaRearSpeed", "RearTTC","RearTTCMinusThreshold",
                "AcceptedGap","SelfSpeed"
            ]
        ] = curData.apply(lambda row2: self.calculateSafetyIndicatros(row1,row2), axis=1, result_type="expand")

        # TET and TIT
        riskTTCLead = curData[curData["LeadTTCMinusThreshold"]!= "None"]
        riskTTCRear = curData[curData["RearTTCMinusThreshold"]!= "None"]

        # TET
        curData["TETLead"] =  len(riskTTCLead) * self.TIMESTEP
        curData["TETRear"] = len(riskTTCRear) * self.TIMESTEP

        # TIT
        curData["TITLead"] = sum(riskTTCLead["LeadTTCMinusThreshold"])
        curData["TITRear"] = sum(riskTTCRear["RearTTCMinusThreshold"])

        self.safetyAnalysisData = pd.concat([self.safetyAnalysisData, curData], axis=0)

    def getMinimumTTCRearAndLead(self, row):
        if row["MergingState"] == False or row["RouteClass"] == "mainline" or row["BreakRuleState"] == "Yes":
            return 999,999,999

        self.outputSafetyData(row)

        conflictdata = {}

        LeadVehicleTTC = 999
        RearVehicleTTC = 999

        LeadVehicle = row["LeadVehicleId"]
        RearVehicle = row["RearVehicleId"]

        TTCLead = self.getTTCList(self.tracksBeforeMerge[self.tracksBeforeMerge["trackId"] == LeadVehicle])
        TTCRear = self.getTTCList(self.tracksBeforeMerge[self.tracksBeforeMerge["trackId"] == RearVehicle])

        if TTCLead != 0 :
            LeadVehicleTTC = min(TTCLead["TTC"])
            conflictdata[LeadVehicle] = TTCLead

        if TTCRear != 0 :
            RearVehicleTTC = min(TTCRear["TTC"])
            conflictdata[RearVehicle] = TTCRear

        if len(conflictdata) != 0:

            return conflictdata, LeadVehicleTTC, RearVehicleTTC
        else:
            return 999, 999,999


    def calculateFlowDensitySpeed(self, curtracks: object, area: object):
        curtracks = curtracks[curtracks["laneletId"].isin(self.HDMdata[area])]
        curtracks.sort_index(inplace=True)

        time = (max(self.tracksSelfInArea123.index.values)-min(self.tracksSelfInArea123.index.values)) * 0.04
        roadlength = sum([self.HDMdata["length"][str(i)] for i in self.HDMdata[area]])
        retangle = time * roadlength

        totaldistance = []
        totaltime = []
        for curvehicle, curgroup in curtracks.groupby("trackId"):
            curgroup.sort_index(inplace=True)

            curdistance = curgroup.iloc[-1, :]["traveledDistance"] - curgroup.iloc[0, :]["traveledDistance"]
            curtime = (curgroup.iloc[-1, :]["frame"] - curgroup.iloc[0, :]["frame"] + 1) * self.TIMESTEP

            totaldistance.append(curdistance)
            totaltime.append(curtime)

        if len(totaldistance) != 0 and len(totaltime) != 0:
            flow = sum(totaldistance) / retangle
            density = sum(totaltime) / retangle
            speed = sum(totaldistance) / sum(totaltime)

            return flow * 3600, density * 1000, speed * 3.6
        else:
            return 0, 0, 0

    def getTrafficFlowDenstiySpeed(self, row):
        if row["MergingState"] == False or row["RouteClass"] == "mainline" or row["BreakRuleState"] == "Yes":
            return 0, 0, 0, 0, 0, 0

        flowarea4, densityarea4, speedarea4 = self.calculateFlowDensitySpeed(self.tracksOtherInTimeArea123,
                                                                                self.metricAreaUpstream)
        flowarea5, densityarea5, speedarea5 = self.calculateFlowDensitySpeed(self.tracksOtherInTimeArea123,
                                                                                self.metricAreaWeaving)

        return flowarea4, densityarea4, speedarea4, flowarea5, densityarea5, speedarea5


    def checkMergingStatus(self, row, tracks,curgroup):

        leftIndex = max(0, row["frame"] - self.LOOKBACK)
        rightIndex = min(max(tracks["frame"]), row["frame"] + self.LOOKBACK)

        tracksLookback = tracks[(tracks["frame"] >= leftIndex) & (tracks["frame"] <= rightIndex)]
        selfLookback = tracksLookback[tracksLookback["trackId"] == row["trackId"]]
        selflanletid = [common.processLaneletData(x, "int") for x in selfLookback["laneletId"].unique()]

        if ((len(set(selflanletid) & set(self.HDMdata["entry"])) != 0)
            and (common.processLaneletData(row["laneletId"], "int") not in self.HDMdata["onramp"])
            and (selfLookback.iloc[0]["latLaneCenterOffset"] > 0)):
            return self.initTracks(tracks, row)

        return False

    def matchSurroundingVehicles(self, row, tracksmeta):
        if row["MergingState"] == False or row["RouteClass"] == "mainline":
            return "None","None","None",\
                   "None","None","None",\
                   "None","None","None",\
                   "None","None","None",\
                   "None","None","None",\
                   "None"

        trajectoryInfo = {}
        RearVehicleNumber = 0
        LeadVehicleNumber = 0
        MinimumRearDistance = 999
        MinimumLeadDistance = 999

        MinimumRearStatus = "None"
        MinimumLeadStatus = "None"
        MinimumRearClass = "None"
        MinimumLeadClass = "None"
        MergingType = "None"
        status = "None"

        RearVehicleSpeed = 999
        LeadVehicleSpeed = 999
        RearHeadway = 999
        LeadHeadway = 999

        LeadVehicleId = "None"
        RearVehicleId = "None"

        for vehicleType in self.surroundingVehiclesLabel:
            vehicleidlistunique = self.tracksSelfInArea123[vehicleType].unique()
            for vehicleId in vehicleidlistunique:

                curinfotail = self.tracksBeforeMerge[self.tracksBeforeMerge["trackId"] == vehicleId].tail(5)
                if vehicleId == -1 or vehicleId == "-999" or curinfotail.empty:
                    continue

                distance = np.sqrt(np.square(row['xCenter'] - curinfotail['xCenter'].mean()) + np.square(
                    row['yCenter'] - curinfotail['yCenter'].mean()))
                speed = (row['xVelocity'] * curinfotail['xVelocity'].mean())

                if distance > self.DISTANCE or speed < 0:
                    continue

                cursurrounidngrouteclass = self.checkVehicleRouteClass(
                    self.tracksBeforeMerge[self.tracksBeforeMerge["trackId"] == vehicleId])
                curLanelet2Id = [common.processLaneletData(x, "int") for x in curinfotail["laneletId"].unique()]

                if len(set(curLanelet2Id) & set(self.HDMdata["-1"])) != 0:
                    positionLabel = "on -1"
                elif len(set(curLanelet2Id) & set(self.HDMdata["-2"])) != 0:
                    positionLabel = "on -2"
                elif len(set(curLanelet2Id) & set(self.HDMdata["-3"])) != 0:
                    positionLabel = "on -3"
                elif len(set(curLanelet2Id) & set(self.HDMdata["entry"])) != 0:
                    positionLabel = "on entry"
                elif len(set(curLanelet2Id) & set(self.HDMdata["onramp"])) != 0:
                    positionLabel = "on onramp"
                else:
                    continue

                if (row["location"] == "2" or row["location"] == "3" or row["location"] == "5") and positionLabel != "on -2":
                    continue
                elif (row["location"] == "6") and positionLabel != "on -3":
                    continue

                if vehicleId in self.alongsidetolead and vehicleType in ["leadId", "leftLeadId", "rightLeadId"] and vehicleId in self.tailLeadVehicles :
                    status = "alongside to lead"

                if vehicleId in self.alongsidetorear and vehicleType in ["rearId", "leftRearId", "rightRearId"] and vehicleId in self.tailRearVehicles :
                    status = "alongside to rear"

                if vehicleId in self.reartofront:
                    leadvehicleFrame = np.append(np.argwhere(self.leadvehicles == vehicleId).flatten() , np.argwhere(self.leftleadvehicles == vehicleId).flatten())
                    rearvehicleFrame = np.append(np.argwhere(self.rearvehicles == vehicleId).flatten() , np.argwhere(self.leftRearvehicles == vehicleId).flatten())

                    if vehicleType in ["leadId", "leftLeadId", "rightLeadId"] and min(leadvehicleFrame) > max(rearvehicleFrame) and vehicleId in self.tailLeadVehicles :
                        status = "rear to lead"
                    elif vehicleType in ["rearId", "leftRearId", "rightRearId"] and max(leadvehicleFrame) < min(rearvehicleFrame) and vehicleId in self.tailRearVehicles :
                        status = "lead to rear"
                    else:
                        status = "WRONG"
                else:
                    status = "Exist"

                if vehicleType in ["rearId", "leftRearId", "rightRearId"]  and vehicleId in self.tailRearVehicles:
                    if distance < MinimumRearDistance:
                        MinimumRearDistance = distance
                        MinimumRearStatus = status
                        MinimumRearClass = tracksmeta[tracksmeta["trackId"] == curinfotail["trackId"].values[0]]["class"].values[0]
                        RearVehicleId= vehicleId
                        RearVehicleSpeed =  np.sqrt(np.square(curinfotail['xVelocity'].mean()) + np.square(curinfotail['yVelocity'].mean()))
                        RearHeadway = MinimumRearDistance / RearVehicleSpeed

                elif vehicleType in ["leadId", "leftLeadId", "rightLeadId"] and vehicleId in self.tailLeadVehicles:
                    if distance < MinimumLeadDistance:
                        MinimumLeadDistance = distance
                        MinimumLeadStatus = status
                        MinimumLeadClass = tracksmeta[tracksmeta["trackId"] == curinfotail["trackId"].values[0]]["class"].values[0]
                        LeadVehicleId= vehicleId
                        LeadVehicleSpeed =  np.sqrt(np.square(row['xVelocity']) + np.square(row['xVelocity']))
                        LeadHeadway = MinimumLeadDistance / LeadVehicleSpeed

                trajectoryInfo[str(vehicleType) + ":" + str(vehicleId)] = {
                    "id": curinfotail["trackId"].values.mean(),
                    "routeclass": cursurrounidngrouteclass,
                    "position": positionLabel,
                    "sidestatus": status,
                    "lonVelocity": curinfotail["lonVelocity"].values.mean(),
                    "latVelocity": curinfotail["latVelocity"].values.mean(),
                    "lonAcceleration": curinfotail["lonAcceleration"].values.mean(),
                    "latAcceleration": curinfotail["latAcceleration"].values.mean(),
                    "distance": distance,
                    "class":
                        tracksmeta[tracksmeta["trackId"] == curinfotail["trackId"].values[0]]["class"].values[
                            0],
                }

        surroudingInfo = {"vehicleNums": len(trajectoryInfo.keys()), "trajectory": trajectoryInfo}

        if MinimumRearStatus == "None" and MinimumLeadStatus == "None":
            MergingType = "A"
        elif MinimumRearStatus == "None" and MinimumLeadStatus == "Exist":
            MergingType = "B"
        elif MinimumRearStatus == "None" and MinimumLeadStatus == "rear to lead":
            MergingType = "C"
        elif MinimumRearStatus == "Exist" and MinimumLeadStatus == "None":
            MergingType = "D"
        elif MinimumRearStatus == "Exist" and MinimumLeadStatus == "Exist":
            MergingType = "E"
        elif MinimumRearStatus == "Exist" and MinimumLeadStatus == "rear to lead":
            MergingType = "F"
        elif MinimumRearStatus == "lead to rear" and MinimumLeadStatus == "None":
            MergingType = "G"
        elif MinimumRearStatus == "lead to rear" and MinimumLeadStatus == "Exist":
            MergingType = "H"

        return surroudingInfo, RearVehicleNumber, MinimumRearDistance,\
               MinimumRearStatus,MinimumRearClass, LeadVehicleNumber, \
               MinimumLeadDistance, MinimumLeadStatus,MinimumLeadClass,\
               MergingType,LeadVehicleId,RearVehicleId,\
               RearVehicleSpeed,RearHeadway,LeadVehicleSpeed,LeadHeadway

    def getMergingDistance(self, row):
        if  row["RouteClass"] != "entry":
            return "None", "None", "None", "None"

        lengthDic = self.HDMdata["length"]
        curHDM = str(common.processLaneletData(row["laneletId"], "int"))
        curlonvalue = common.processLaneletData(row["lonLaneletPos"], "float")
        mergingdistance = "None"
        mergingdistanceratio = "None"

        if row["location"] == "2":
            if curHDM == "1499":
                mergingdistance = -float(lengthDic["1499"]) + curlonvalue
            elif curHDM == "1502":
                mergingdistance = curlonvalue
            elif curHDM == "1574":
                mergingdistance = float(lengthDic["1502"]) + float(curlonvalue)

        elif row["location"] == "3":
            if curHDM == "1414":
                mergingdistance = -float(lengthDic["1414"]) + curlonvalue
            elif curHDM == "1524":
                mergingdistance = curlonvalue
            elif curHDM == "1528" or curHDM == "1530":
                mergingdistance = float(lengthDic["1524"]) + float(curlonvalue)
            elif curHDM == "1422":
                mergingdistance = float(lengthDic["1524"]) + float(lengthDic["1528"]) + float(curlonvalue)

        elif row["location"] == "4":
            if curHDM == "1451" or curHDM == "1452":
                mergingdistance = -float(lengthDic["1451"]) + curlonvalue
            elif curHDM == "1455" or curHDM == "1456":
                mergingdistance = curlonvalue
            elif curHDM == "1459" or curHDM == "1460":
                mergingdistance = float(lengthDic["1455"]) + float(curlonvalue)

        elif row["location"] == "5":
            if curHDM == "1408":
                mergingdistance = -float(lengthDic["1408"]) + curlonvalue
            elif curHDM == "1411":
                mergingdistance = curlonvalue
            elif curHDM == "1414":
                mergingdistance = float(lengthDic["1411"]) + curlonvalue

        elif row["location"] == "6":
            if curHDM == "1459":
                mergingdistance = -float(lengthDic["1459"]) + curlonvalue
            elif curHDM == "1463":
                mergingdistance = curlonvalue
            elif curHDM == "1467":
                mergingdistance = float(lengthDic["1463"]) + curlonvalue

        obeyRule = "None"
        obeyArea = "None"

        if mergingdistance != "None":
            mergingdistanceratio = mergingdistance / self.locationTotalMergingDistance[row["location"]]

            if mergingdistanceratio > 1:
                obeyRule = "Yes"
                obeyArea = "area 4"
            elif mergingdistanceratio <= 0:
                obeyRule = "Yes"
                obeyArea = "area 1"

        return mergingdistance, mergingdistanceratio, obeyRule, obeyArea

    def getMergingDuration(self, row):
        if row["MergingState"] == False or row["RouteClass"] == "mainline" or row["BreakRuleState"] == "Yes":
            return 0
        return len(self.tracksSelfInArea23) * 0.04

    def calculateConsecutiveLanechange(self, gaplist, tmpconcat):

        type, time = "None", "None"
        onrampState = tmpconcat["MergingState"].values

        if np.where(onrampState == True)[0].size != 0:
            indexTrue = np.where(onrampState == True)[0][0]
            if np.where(onrampState[indexTrue:] == False)[0].size == 0:
                type = 1
                time = "None"
            else:
                falseIndex = np.where(onrampState[indexTrue:] == False)[0][0]
                type = 2
                time = (gaplist[indexTrue + falseIndex] - gaplist[indexTrue]) * 0.04

        return type, time

    def getLateralSpeedandAcceleration(self, row):
        if row["MergingState"] == False or row["RouteClass"] == "mainline" or row["BreakRuleState"] == "Yes":
            return "None", "None", "None"

        selfdata = self.tracksSelfInArea123
        values = selfdata["latLaneCenterOffset"].values

        if len(values) >20:
            values = values[-20:]

        try:
            x, y = np.arange(0, len(values)), values
            p = np.poly1d(np.polyfit(x, y, 5))
            dfx = p.deriv()
            ddfx = dfx.deriv()
            speed, acceleration = [dfx(i) for i in x], [ddfx(i) for i in x]

            return max(speed) / 0.04, max(acceleration) / 0.04, min(acceleration) / 0.04
        except:

            return "None", "None", "None"

    def checkVehicleRouteClass(self, data):
        curlaneletId = self.getAllLaneletId(list(set(data["laneletId"].unique())))
        onrampstatus = set(curlaneletId) & set(self.HDMdata["onramp"])
        offrampstatus = set(curlaneletId) & set(self.HDMdata["exit"])
        mainlineupstreamstatus = set(curlaneletId) & set(self.HDMdata["mainlineUpstream"])

        if len(onrampstatus) != 0 and len(mainlineupstreamstatus) == 0:
            return "entry"
        if len(offrampstatus) != 0:
            return "exit"
        if len(onrampstatus) == 0 and len(offrampstatus) == 0 and len(mainlineupstreamstatus) != 0:
            return "mainline"
        else:
            return "wrong"

    def readCSVFile(self, curTracksId):

        PathTracksMeta = self.rootPath + "/drone-dataset-tools-master/data/" + str(curTracksId) + "_tracksMeta.csv"
        PathRecordingMeta = self.rootPath + "/drone-dataset-tools-master/data/" + str(
            curTracksId) + "_recordingMeta.csv"
        PathTracks = self.rootPath + "/drone-dataset-tools-master/data/" + str(curTracksId) + "_tracks.csv"

        tracks = pd.read_csv(PathTracks, low_memory=False)
        tracksMeta = pd.read_csv(PathTracksMeta)
        recordingMeta = pd.read_csv(PathRecordingMeta)

        logger.info("Loading recording {} ", curTracksId)
        logger.info("Loading csv{}, {} and {}", PathTracksMeta, PathRecordingMeta, PathTracks)

        xUtmOrigin = recordingMeta["xUtmOrigin"].values[0]
        yUtmOrigin = recordingMeta["yUtmOrigin"].values[0]

        tracks["curxglobalutm"] = tracks["xCenter"].apply(lambda x: x + xUtmOrigin)
        tracks["curyglobalutm"] = tracks["yCenter"].apply(lambda x: x + yUtmOrigin)

        tracks.fillna("-999", inplace=True)
        tracks.astype({"trackId": "int"}, )

        return tracks, tracksMeta, recordingMeta

    def getAllLaneletId(self, string):
        string_new = []
        for cur_string in string:
            if ";" not in str(cur_string):
                string_new.append(int(cur_string))
            elif ";" in str(cur_string):
                for i in cur_string.split(";"):
                    string_new.append(int(i))
        return string_new
