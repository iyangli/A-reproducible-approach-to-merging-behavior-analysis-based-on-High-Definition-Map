import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import json
import cv2
import matplotlib

pd.set_option('max_colwidth',200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

root_path = os.path.abspath('../../../')


ortho_px_to_meter = 0.100000000000002
with open(root_path+"/conf/visualizer_params.json") as f:
    dataset_params = json.load(f)

dataset_params = dataset_params["exid"]

data_path = root_path+"/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)
mergingData = ori_data[(ori_data['MergingState']==True) & (ori_data['RouteClass']=='entry') ]
mergingData["xCenterVis"] = mergingData["xCenter"] / ortho_px_to_meter
mergingData["yCenterVis"] = -mergingData["yCenter"] / ortho_px_to_meter
mergingData["xCenterVis"] = mergingData["xCenterVis"]/dataset_params["scale_down_factor"]
mergingData["yCenterVis"] = mergingData["yCenterVis"]/dataset_params["scale_down_factor"]


FONTSIZE = 10

for curlocation in range(2,7):
    if curlocation == 4:
        continue

    curLoctionTwo = mergingData[mergingData["location"] == curlocation]
    curLocationCar = curLoctionTwo[curLoctionTwo["vehicleClass"]=="car"]
    curLocationTruck = curLoctionTwo[curLoctionTwo["vehicleClass"]=="truck"]
    curLocationVan = curLoctionTwo[curLoctionTwo["vehicleClass"]=="van"]

    if curlocation == 2:
        xlimits = [1000,1300]
        ylimits = [800,400]
        length = 10
        width = 4

    elif curlocation == 3:
        xlimits = [300,800]
        ylimits = [500,200]
        length = 10
        width = 4

    elif curlocation == 4:
        xlimits = [400, 1000]
        ylimits = [600, 200]
        length = 10
        width = 5

    elif curlocation == 5:
        xlimits = [600, 1020]
        ylimits = [420, 350]
        length = 10
        width = 3

    elif curlocation == 6:
        xlimits = [300, 800]
        ylimits = [400, 300]
        length = 10
        width = 3


    curBackgroundPicture = root_path + "/asset/backgroundPicture/" + str(curlocation) + ".png"
    background_image = cv2.cvtColor(cv2.imread(curBackgroundPicture), cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(length, width), constrained_layout=True)

    ax1 = plt.subplot(2,2,1)
    ax1.imshow(background_image, zorder=1, aspect='auto')
    ax1.set_xlim(xlimits)
    ax1.set_ylim(ylimits)
    ax1.scatter(curLoctionTwo["xCenterVis"], curLoctionTwo["yCenterVis"],s=1, c='black', marker='o', zorder=3)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("total",fontsize=FONTSIZE)
    plt.xlabel("a) x position",fontsize = FONTSIZE)
    plt.ylabel("y position",fontsize = FONTSIZE)
    ax1.set(xlabel=None)

    ax2 = plt.subplot(2,2,2)
    ax2.imshow(background_image, zorder=1, aspect='auto')
    ax2.set_xlim(xlimits)
    ax2.set_ylim(ylimits)
    ax2.scatter(curLocationCar["xCenterVis"], curLocationCar["yCenterVis"], s=1, c='r', marker='<', zorder=3)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("car",fontsize=FONTSIZE)
    plt.xlabel("b) x position",fontsize = FONTSIZE)
    plt.ylabel("y position",fontsize = FONTSIZE)
    ax2.set(xlabel=None)

    ax3 = plt.subplot(2,2,3)
    ax3.imshow(background_image, zorder=1,aspect='auto')
    ax3.set_xlim(xlimits)
    ax3.set_ylim(ylimits)
    ax3.scatter(curLocationTruck["xCenterVis"], curLocationTruck["yCenterVis"], s=1, c='b', marker='*', zorder=4)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("truck",fontsize=FONTSIZE)
    plt.xlabel("c) x position",fontsize = FONTSIZE)
    plt.ylabel("y position",fontsize = FONTSIZE)
    ax3.set(xlabel=None)

    ax4 = plt.subplot(2,2,4)
    ax4.imshow(background_image, zorder=1,aspect='auto')
    ax4.set_xlim(xlimits)
    ax4.set_ylim(ylimits)
    ax4.scatter(curLocationVan["xCenterVis"], curLocationVan["yCenterVis"], s=1, c='g', marker='v', zorder=4)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("van",fontsize=FONTSIZE)
    plt.xlabel("d) x position",fontsize = FONTSIZE)
    plt.ylabel("y position",fontsize = FONTSIZE)
    ax4.set(xlabel=None)

    plt.tight_layout()
    plt.savefig(root_path+"/asset/preliminaryAnalysis/mergingPointScatter "+str(curlocation)+".png", dpi=800)
    plt.close()









