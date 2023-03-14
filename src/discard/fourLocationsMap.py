import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import json
import cv2
import matplotlib
from matplotlib import gridspec

pd.set_option('max_colwidth',200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

root_path = os.path.abspath('../../')


ortho_px_to_meter = 0.100000000000002
with open(root_path+"/conf/visualizer_params.json") as f:
    dataset_params = json.load(f)

dataset_params = dataset_params["exid"]

# read file
data_path = root_path+"/asset/mergingData.csv"
ori_data = pd.read_csv(data_path)
mergingData = ori_data[ori_data['RouteClass']=='entry']

mergingData["xCenterVis"] = mergingData["xCenter"] / ortho_px_to_meter
mergingData["yCenterVis"] = -mergingData["yCenter"] / ortho_px_to_meter
mergingData["xCenterVis"] = mergingData["xCenterVis"]/dataset_params["scale_down_factor"]
mergingData["yCenterVis"] = mergingData["yCenterVis"]/dataset_params["scale_down_factor"]


fig = plt.figure(figsize=(9, 6), constrained_layout=True)

spec = gridspec.GridSpec(ncols=2, nrows=2, width_ratios=[1, 1], height_ratios=[3,1])

third = {"2":1,"3":2,"5":3,"6":4}

FONTSIZE = 10

for curlocation in [2,3,5,6]:

    curLoction = mergingData[mergingData["location"] == curlocation]

    limits = dataset_params["relevant_areas"][str(curlocation)]
    limits["x_lim"][0] = int(limits["x_lim"][0] / dataset_params["scale_down_factor"])
    limits["x_lim"][1] = int(limits["x_lim"][1] / dataset_params["scale_down_factor"])
    limits["y_lim"][0] = int(limits["y_lim"][0] / dataset_params["scale_down_factor"])
    limits["y_lim"][1] = int(limits["y_lim"][1] / dataset_params["scale_down_factor"])

    curBackgroundPicture = root_path + "/asset/backgroundPicture/" + str(curlocation) + ".png"
    background_image = cv2.cvtColor(cv2.imread(curBackgroundPicture), cv2.COLOR_BGR2RGB)

    ax1 = plt.subplot(spec[third[str(curlocation)]-1])
    ax1.imshow(background_image, zorder=1, aspect="auto")
    ax1.set_xlim(limits["x_lim"])
    ax1.set_ylim(limits["y_lim"])
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.title("Location "+str(curlocation),fontsize=FONTSIZE)
    plt.xlabel(chr(third[str(curlocation)]+96)+") x position",fontsize = FONTSIZE)
    plt.ylabel("y position",fontsize = FONTSIZE)

plt.tight_layout()
plt.savefig(root_path+"/asset/preliminaryAnalysis/fourLocationMap.png", dpi=800)


