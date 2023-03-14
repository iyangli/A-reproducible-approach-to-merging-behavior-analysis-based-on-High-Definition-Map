
import math
import numpy as np

def filterLaneChange(curLcIndex):
    gaplist = []
    tepIndex = []
    if len(curLcIndex) == 1:
        gaplist.append(-1)
    else:
        for i in range(len(curLcIndex) - 1):
            gap = round((curLcIndex[i + 1] - curLcIndex[i]) / 25, 2)
            gaplist.append(gap)
        for j in range(len(gaplist)):
            if gaplist[j] < 1:
                tepIndex.append(j)
            else:
                continue
        curLcIndex = np.delete(curLcIndex, tepIndex)

    return curLcIndex

def calculateLonVelocity(row, direction, variable):
    angle = math.radians(row["heading"])
    cosvalue = math.cos(angle)
    sinvalue = math.sin(angle)
    first = "x" + variable
    second = "y" + variable

    if direction == "lon":
        return row[first] * cosvalue + row[second] * sinvalue
    elif direction == "lat":
        return row[first] * sinvalue - row[second] * cosvalue

def processLaneletData(row, type):
    if type == "int":
        if ";" not in str(row):
            return int(row)
        else:
            return int(row.split(";")[0])
    elif type == "float":
        if ";" not in str(row):
            return float(row)
        else:
            return float(row.split(";")[0])
