import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

root_path = os.path.abspath('../../../')
data_path = root_path+"/asset/mergingData100m.csv"
ori_data = pd.read_csv(data_path)

mergingData = ori_data[(ori_data['MergingState']==True) & (ori_data['RouteClass']=='entry') & (ori_data['BreakRuleState']=='None') & (ori_data['MergingDistance'] !='None')  & (ori_data['MaxLateralSpeed'] !='None') ]
mergingData['MergingDistance'] = mergingData['MergingDistance'].astype('float')
mergingData['MergingDuration'] = mergingData['MergingDuration'].astype('float')
mergingData['MaxLateralSpeed'] = mergingData['MaxLateralSpeed'].astype('float')
mergingData['MaxiLateralAcc'] = mergingData['MaxiLateralAcc'].astype('float')
mergingData['MergingDistanceRatio'] = mergingData['MergingDistanceRatio'].astype('float')
mergingData['totalvelocity'] = np.sqrt(np.square(mergingData['xVelocity'])+np.square(mergingData['yVelocity']))

mergingData.sort_values(by="vehicleClass", inplace=True)
mergingData.replace({"location":{2:"location2",3:"location3",5:"location5",6:"location6"}},inplace=True)

font1 = {
    'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 14,
}

FONTSIZE = 14
plt.figure(figsize=(12, 12))
plt.style.use('seaborn-colorblind')

ax1 = plt.subplot(321)
sns.boxplot(x="location", y="totalvelocity",data=mergingData,hue = "vehicleClass",showmeans=True,whis = 3,notch=True,
            order=["location2","location3","location5","location6"],meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([10,15,20,25,30,35,40,45])
plt.ylabel("Speed(m/s)",font1)
plt.grid(ls='-',axis="both")
plt.title("Merging Speed",font1)
plt.legend(prop=font1)
sns.set_context("notebook")
ax1.set(xlabel=None)

ax2 = plt.subplot(322)
sns.boxplot(x="location", y="MergingDistance", data=mergingData,hue = "vehicleClass",showmeans=True,whis = 3,notch=True,
            order=["location2", "location3", "location5", "location6"],meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,25,50,75,100,125,150,175,200,225,250])
plt.ylabel("Distance(m)", font1)
plt.grid(ls='-',axis="both")
plt.title("Merging distance",font1)
ax2.get_legend().remove()
sns.set_context("notebook")
ax2.set(xlabel=None)

ax3 = plt.subplot(323)
sns.boxplot(x="location", y="MergingDistanceRatio", data=mergingData,hue = "vehicleClass",showmeans=True,whis = 3,notch=True,
            order=["location2","location3","location5","location6"],meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,0.2,0.4,0.6,0.8,1,1.2,1.4])
plt.ylabel("Ratio", font1)
plt.grid(ls='-',axis="both")
plt.title("Merging distance ratio",font1)
ax3.get_legend().remove()
sns.set_context("notebook")
ax3.set(xlabel=None)

ax4 = plt.subplot(324)
sns.boxplot(x="location", y="MergingDuration", data=mergingData,hue = "vehicleClass",showmeans=True,whis = 3,notch=True,
            order=["location2","location3","location5","location6"],meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,2,4,6,8,10,12,14])
plt.ylim([0,14])
plt.ylabel("Time(s)", font1)
plt.grid(ls='-',axis="both")
plt.title("Merging duration",font1)
ax4.get_legend().remove()
sns.set_context("notebook")
ax4.set(xlabel=None)

ax5 = plt.subplot(325)
sns.boxplot(x="location", y="MaxLateralSpeed", data=mergingData,hue = "vehicleClass",showmeans=True,whis = 3,notch=True,
            order=["location2","location3","location5","location6"],meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,0.5,1,1.5,2,2.5,3,3.5])
plt.ylabel("Speed(m/s)", font1)
plt.grid(ls='-',axis="both")
plt.title("Merging maximum lateral speed",font1)
ax5.get_legend().remove()
sns.set_context("notebook")
ax5.set(xlabel=None)

ax6 = plt.subplot(326)
sns.boxplot(x="location", y="MaxiLateralAcc", data=mergingData,hue = "vehicleClass",showmeans=True,whis = 3,notch=True,
            order=["location2","location3","location5","location6"],meanprops = {'marker':'D','markerfacecolor':'red'},palette="hls",saturation=0.6, showfliers = True)
plt.xticks(fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
plt.ylim([0,1])
plt.ylabel("Acceleration(m/s$^{2}$)", font1)
plt.grid(ls='-',axis="both")
plt.title("Merging maximum lateral acceleration",font1)
ax6.get_legend().remove()
sns.set_context("notebook")
ax6.set(xlabel=None)

plt.tight_layout()

plt.savefig(root_path+"/asset/preliminaryAnalysis/mergingSpeedPointDuration.png", dpi=600)


