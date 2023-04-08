import argparse
from loguru import logger
import pandas as pd

class vehicleTrajectoryClass(object):
    def __init__(self,config,trajectory):
        self.config = config
        self.vehicleId = config["vehicleId"]
        self.locationId = config["locationId"]
        self.startTime = config["startTime"]
        self.endTime = config["endTime"]
        self.vehicleClass = config["vehicleClass"]
        self.trajectoryDic = trajectory

    def getTrajectory(self,time):

        return self.trajectoryDic.loc[time]["xPosition"],self.trajectoryDic.loc[time]["yPosition"]

def createArgs():
    cs = argparse.ArgumentParser(description="get vehicle trajectory")

    cs.add_argument('--vehicleId', default=1, help="vehicle id", type=int)
    cs.add_argument('--locationId', default=1,help="location id", type=int)
    cs.add_argument('--startTime', default=1,help="start time", type=int)
    cs.add_argument('--endTime', default=10,help="start time", type=int)
    cs.add_argument('--vehicleClass', default="vehicle",help="vehicleClass", type=str)

    return vars(cs.parse_args())

def main():
    exampleTrajectory = pd.DataFrame()
    time = 0.5

    config = createArgs()
    logger.info("initial trajectory")
    trajectory = vehicleTrajectoryClass(config,exampleTrajectory)

    logger.info("get position")
    xPosition,yPosition = trajectory.getTrajectory(time)
    logger.info("current xPosition {}, yPosition is {}",xPosition,yPosition)

if __name__ == '__main__':
    main()

