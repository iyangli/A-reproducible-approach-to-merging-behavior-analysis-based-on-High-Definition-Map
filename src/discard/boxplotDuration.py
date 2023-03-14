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

for i in [100,150,200]:
    data_path = root_path + "/asset/mergingData" + str(i) + "m.csv"
    ori_data = pd.read_csv(data_path)

    mergingData = ori_data[
        (ori_data['MergingState']==True)
        & (ori_data['RouteClass']=='entry')
        & (ori_data['BreakRuleState']=='None')
        & (ori_data['MergingDistance'] !='None')
        & (ori_data['MaxLateralSpeed'] !='None')
        & (ori_data['MergingType'] != 'None')
        ]

    mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
    mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
    mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
    mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
    mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
    mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))

    mergingData.sort_values(by="vehicleClass", inplace=True)

    ax1 = plt.subplot(3,4,4*j+1)
    g1 = sns.boxplot(x="MergingType", y="MergingDuration",data=mergingData[mergingData["location"]==2],hue = "vehicleClass",showmeans=True,whis = 3,
                order=["A", "B", "C","D", "E", "F","G"], meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)

    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0, 2, 4, 6, 8, 10, 12])
    plt.ylim([0, 12])
    # plt.xlabel("a) merging scenario",font1)
    g1.set(xlabel=None)
    plt.ylabel("Time(s)", font1)
    plt.grid(ls='-',axis="both")
    plt.title("DISTANCE="+str(i)+",location"+str(2),font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    ax2 = plt.subplot(3,4,4*j+2)
    g2 = sns.boxplot(x="MergingType", y="MergingDuration",data=mergingData[mergingData["location"]==3],hue = "vehicleClass",showmeans=True,whis = 3,
                order=["A", "B", "C","D", "E", "F","G"], meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0, 2, 4, 6, 8, 10, 12])
    plt.ylim([0, 12])
    # plt.xlabel("b) merging scenario",font1)
    g2.set(xlabel=None)
    plt.ylabel("Time(s)", font1)
    plt.grid(ls='-',axis="both")
    plt.title("DISTANCE="+str(i)+",location"+str(3),font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    ax3 = plt.subplot(3,4,4*j+3)
    g3 = sns.boxplot(x="MergingType", y="MergingDuration",data=mergingData[mergingData["location"]==5],hue = "vehicleClass",showmeans=True,whis = 3,
                order=["A", "B", "C","D", "E", "F","G"], meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)

    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0, 2, 4, 6, 8, 10, 12])
    plt.ylim([0, 12])
    # plt.xlabel("c) merging scenario",font1)
    g3.set(xlabel=None)
    plt.ylabel("Time(s)", font1)
    plt.grid(ls='-',axis="both")
    plt.title("DISTANCE="+str(i)+",location"+str(5),font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    ax4 = plt.subplot(3,4,4*j+4)
    g4 = sns.boxplot(x="MergingType", y="MergingDuration",data=mergingData[mergingData["location"]==6],hue = "vehicleClass",showmeans=True,whis = 3,
                order=["A", "B", "C","D", "E", "F","G"], meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.yticks([0, 2, 4, 6, 8, 10, 12])
    plt.ylim([0, 12])
    # plt.xlabel("d) merging scenario",font1)
    g4.set(xlabel=None)
    plt.ylabel("Time(s)", font1)
    plt.grid(ls='-',axis="both")
    plt.title("DISTANCE="+str(i)+",location"+str(6),font1)
    sns.set_context("notebook")
    plt.legend(prop=fontlegend)

    j += 1


plt.tight_layout()
# plt.show()
plt.savefig(root_path+"/asset/JSDivergence/BoxplotDuration.png", dpi=800)
# plt.clf()
