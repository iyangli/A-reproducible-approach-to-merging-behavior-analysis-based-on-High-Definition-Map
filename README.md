

# 车辆与车流数据挖掘

## 1 项目

### 1.1 介绍

交通学科：

车辆/控制/信息学科：


随着信息技术不断发展，获取连续高精度车辆轨迹得以成为可能，从而使得全面深入挖掘车辆轨迹成为可能  

成立缘由：
- 国内外虽有很多做过车流轨迹数据的研究，但这些研究均为像本项目这样全面
- 国内缺乏这样的教材，结合模型与数据
- 所有的研究缺乏可复现性

意义
- 任何人可以复现所有的代码
- 在此基础上开展进一步的挖掘
- 为自动驾驶车辆提供基础的数据挖掘


### 1.2 主要工作
- 现有数据集介绍
  - NGSIM数据集
  - HighD数据集
  - Exit数据集
  - 其他数据集


- 典型驾驶场景：
  - carfollowing
  - lanechanging
  - cutin
  - crossing
  - merging
  - weaving


- 场景提取规则：
  - carfollowing
  - lanechanging
  - cutin
  - crossing
  - merging
  - weaving


- 数据挖掘：
  - 轨迹去噪，轨迹平滑算法
  - 起始点确定算法
  - 交通流分析
  - 驾驶行为分析
    - 跟驰模型基准分析
    - 跟驰模型模型标定
    - 驾驶风格量化
    - 不同类型车辆
  - 风险与安全评估
  - 轨迹预测算法
  - 交互量化算法
  - 场景范参数化



### 1.3 环境配置

本项目所有的内容都采用的是`Python`语言  
有意向的开发者可以使用git工具协同开发

##### conda常用命令
```
# 创建 VTM (Vehicle Trajectory Mining) 环境
conda create --name VTM python=3.7

# 激活环境
conda activate VTM
python --version

# 常用指令
conda info --envs
conda list
conda env export > environment.yml

#查看源以及添加源
conda config --show channels
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --set show_channel_urls yes
```

##### git常用命令
```
# 克隆仓库
git clone <远程仓库>
git clone <远程仓库> <本地>
git clone <远程仓库> -b <分支名称> <本地>

# 初始化与查看仓库状
git init
git status

# 查看远程
git remote
git remote -v
git remote rename <原远程仓库> <新名>
git remote set-url <旧名> <新名>

# 分支操作
git branch
git branch <新分支>
git branch -m [<原分支>] <新分支>
git checkout <分支>
git checkout <文件>

# 提交操作
git add .
git commit -m "<描述信息>"
git commit -a -m "<描述信息>"
git merge <分支名称>

#其他
git diff
git diff <分支> <分支>
git log
git reset --mixed [<文件路径>]
git reset --mixed <commit ID>
git reset --hard <commit ID>
git reset --soft <commit ID>

```
[可以查看这篇帖子](https://blog.csdn.net/qq_41627844/article/details/107034680)

### 1.4 目录架构

1. src: 放入所有的代码
2. asset：所有的分析结果
3. conf：项目的配置文件
4. doc：代表性论文及使用手册
5. util：使用工具

### 1.5 研究基础
知识基础
1.  交通流理论
2.  统计、计算机

工具基础
1. Tools: python语言，git工具，
2. Package: pandas、scipy、numpy、opencv等


## 3 数据集
以下介绍Exit以及HighD数据集

### 3.1 ExiD 说明 

以下为该数据集所采集的六个地点车辆、

<img src="asset/datasetPreprocess/ExiD/LocationWeekdayClassCount/class.png" width="400">
<img src="asset/datasetPreprocess/ExiD/LocationWeekdayClassCount/classRecording.png" width="400">

[原图在这](asset/datasetPreprocess/ExiD)


### 3.2 HighD 说明
* HighD数据集，该数据集采集于2017年及2018年的德国高速公路，该数据集包含16.5小时的测量，共计有45000公里的总行驶距离和超过11000辆车辆。这些轨迹是以4k（4096*2160）的分辨率，从德国科隆附近的六个不同地点记录。同时，每条轨迹的定位误差小于10厘米。与NGSIM数据集相比，该数据集更适合于对高度自动驾驶系统进行系统级验证； 
* 下图给出了轨迹采集的说明、无人机的俯视图以及数据采集的六个地点。数据格式如下图所示所示，其字段有：当前帧、车辆id、位置信息、宽度与长度、横向与纵向速度、横向与纵向加速度、车头时距、车头间距、前后车辆id、左右车辆id以、车道id、车辆类型、最大最小速度、最大最小加速度、行驶方向、最小最大车头间距、最小最大车头时距以及是否换道（0或1）。

[//]: # (<img src="asset/dataset/HighD/HighD dataset Description.png" width="400" alt="value">)


## 4 场景提取

### 4.1 高精度地图 

#### Lanelet2 
Lanelet2地图采用分层结构，可以分为：物理层、关联层、拓扑层

Point点: 由ID，3d坐标和属性组成，是唯一存储实际位置信息的元素，ID必须唯一;

LineString线串: 两个或者多个点构成的序列，描述地图元素的形状。可以是虚线，可以通过高度离散化实现，来描述任何一维形式，并应用于地图上的任何可物理观察到的部分。线串可以高效计算，并且可以用来描述尖角。线串可以是区分方向的也可以是不区分方向的，可以是闭合的也可以是非闭合的。

Lanelet车道: 定义了发生定向运动时，地图车道的原子部分。原子表示沿当前lanelet行驶时，有效的交通规则不会改变，而且与其他Lanelet的拓扑关系也不会更改。lanelet可以引用表示适用于该lanelet的交通规则的regulatory element。多个lanelet可以引用同一regulatory element。必须始终可以直接从车道上确定车道的当前速度限制。

Area区域: Area是地图上没有方向或者是无法移动的部分区域，比如路标，停车位，绿化带等。由一条或者多条linestring组成的闭合的区域。Area也有相关联的regulatory element。

Polygon多边形:   多边形与线串非常相似，但形成一个Area。隐式假定多边形的第一个点和最后一个点被连接以闭合形状。多边形很少用于传输地图信息（交通标志除外）。相反，它们通常用作将有关区域的自定义信息添加到地图的一种手段。

Regulatory Element：  Regulatory Element是表达交通规则的通用方式，在应用的时候，Regulatory Element会和一个或者多个Lanelet、Area相关联。Regulatory Element是动态变化的，意味着它只是在某些条件下是有效的。诸如限速，道路优先级规则、红绿灯等，交通规则有许多不同的类型，因此每个Regulatory Element的准确结构大都不一样。他们通常引用定义规则的元素（例如交通标志），并在必要时引用取消规则的元素。

Lanelet2高精地图采用.OSM文件来表示

OpenStreetMap的元素（数据基元）主要包括三种：点（Nodes）、路（Ways）和关系（Relations），这三种原始构成了整个地图画面。其中，Nodes定义了空间中点的位置；Ways定义了线或区域；Relations（可选的）定义了元素间的关系。


高精地图的绝对精度一般都会在亚米级，以高德地图为例，绝对精度可以达到10厘米以内，而且横向的相对精度往往还要更高。  
高精地图不仅有高精度的坐标，同时还有准确的道路形状，并且每个车道的坡度、曲率、航向、高程，侧倾的数据也都包含在内。

#### Opendrive
OpenDRIVE是目前国际上较通用的一种格式规范，由一家德国公司制定。在运用OpenDRIVE格式规范表述道路时，会涉及Section、Lane、Junction、Tracking四个概念。

无论车道线变少或变多，都是从中间的灰线切分。切分之后的地图分为Section A、Section B和Section C三部分。一条道路可以被切分为很多个Section。按照道路车道数量变化、道路实线和虚线的变化、道路属性的变化的原则来对道路进行切分。

在第二个Lane概念中，Reference Line在OpenDRIVE规范中非常重要。没有Reference Line，可以说一事无成。基于Reference Line，向左表示ID向左递增，向右表示ID向右递减，它是格式规范的标准之一，同时也是固定的、不可更改的。比如，Reference Line的ID为0，向左是1、2、3，向右是−1、−2、−3。

Junction是OpenDRIVE格式规范中的路口概念。Junction中包含虚拟路，虚拟路用来连接可通行方向，用红色虚线来表示。在一张地图中，在遇到对路口的表述时，虽然说路口没有线，但我们要用虚拟线来连接道路的可通行方向连，以便无人驾驶车辆明确行进路线

以上三个概念在OpenDRIVE格式规范中，是基于Reference Line条件下应用，还有基于Reference Line和偏移量条件下的应用，其中十分重要的一个概念叫做Tracking。Tracking的坐标系是ST，S代表车道Reference Line起点的偏移量，T代表基于Reference Line的横向偏移量。前者是纵向的，后者是横向的。

OpenDRIVE格式使用文件拓展名为xodr的可扩展标记语言（XML）作为描述路网的基础。存储在OpenDRIVE文件中的数据描述了道路的几何形状以及可影响路网逻辑的相关特征(features)，例如车道和标志。OpenDRIVE中描述的路网可以是人工生成或来自于真实世界的。OpenDRIVE的主要目的是提供可用于仿真的路网描述，并使这些路网描述之间可以进行交换。

该格式将通过节点(nodes)而被构建，用户可通过自定义的数据扩展节点。这使得各类应用（通常为仿真）具有高度的针对性，同时还保证不同应用之间在交换数据时所需的互通性。


#### Opendrive
.xodr文件可以用在线网页http://opendrive.bimant.com/打开Opendrive地图，这里需要注意

![](asset/figure/lanelet2.jpg)



### 换道场景
我们首先结合LaneLet2格式的高精地图对每个location的laneID的类型进行标注，结合数据集tracks的[lane]给车辆打上标签：onramp（上匝道），offramp（下匝道），driving（主路行驶）。


```

根据相对路径读取本地数据文件夹，循环读取每个文件


















```






#### 紧密换道场景







###  研究基础





#### 5.0 






#### 5.0 




### Personal Info 
Author: Yang Li  
Email: yangli.chn@outlook.com  
Major: Transportation Engineering  
2018.09.01~2024.03.01(expected graduation date), Ph.D., Candidate in Tongji University, supervisor: Linbo Li and Daiheng Ni  
2022.06.15~2022.09.30, Internship in the AI group of Huawei Autonomous Driving Solutions' PNC department, supervisor: Chao Wang

SCI在投与工作

1. Yang Li, Linbo Li(通讯), Daiheng Ni. Pareto-optimal lane-changing trajectory planning in mixed traffic, Submitted to IEEE Transactions on Intelligent Transportation Systems. (SCI；影响因子9.55；自主换道轨迹规划；三审)

2. Yang Li, Linbo Li(通讯), Daiheng Ni. Dynamic trajectory planning for automated lane-changing, Submiteed to Journal of Advanced Transportation.(SCI；影响因子2.24；自主换道轨迹规划)

3. Yang Li, Linbo Li(通讯), Daiheng Ni. Application of Gaussian Mixture Model for Clustering Analysis of High-Risk Cut-In Scenarios Based on HighD Dataset, Submiteed to Sustainbility. (SCI；影响因子3.889；换道轨迹挖掘)

4. Yang Li, Linbo Li, Daiheng Ni. Understanding the merging behavior: towards transparency and reproducibility


SCI收录

1. Yang Li, Linbo Li(通讯), Daiheng Ni, Wenxuan Wang. Automatic lane-changing motion planning: from self-optimum to local-optimum, IEEE Transactions on Intelligent Transportation Systems , 2022, doi:10.1109/TITS.2022.3179117.(SCI；影响因子9.55；自主换道轨迹规划）

2. Yang Li, Linbo Li(通讯), Daiheng Ni, Yue Zhang. Comprehensive survival analysis of lane-changing duration, Measurement, 2021, 182, 109707.(SCI；影响因子5.13；换道行为数据挖掘)

3. Yang Li, Linbo Li(通讯), Daiheng Ni. Comparative univariate and regression survival analysis of lane-changing duration characteristic for heavy vehicles and passenger cars, Journal of Transportation Engineering, Part A: Systems, 2022, doi: 10.1061/JTEPBS.0000771. (SCI；影响因子1.93；换道行为数据挖掘)

4. Linbo Li, Yang Li(通讯), Daiheng Ni. Incorporating human factors into LCM using fuzzy TCI model. Transportmetrica B: Transport Dynamics, 2021, 9, 198-218.(SCI；影响因子3.41；跟车行为建模与数据挖掘)


会议论文

1. Yang Li, Linbo Li(通讯), Daiheng Ni, Wenxuan Wang. Hierarchical automatic lane-changing motion planning: from self-optimum to local-optimum, 2022, the 101th annual meeting of the transportation research board, Washington, DC.

2. Yang Li, Linbo Li(通讯), Daiheng Ni. Comparative univariate and regression survival analysis of lane-changing duration based on the HighD dataset, 2022, the 101th annual meeting of the transportation research board, Washington, DC.

3. Yang Li, Linbo Li(通讯), Daiheng Ni. Exploration of lane-changing duration for heavy vehicles and passenger cars: a survival analysis approach, 2022, the 101th annual meeting of the transportation research board, Washington, DC.

4. Yang Li, Linbo Li(通讯), Daiheng Ni, Yue Zhang. Comprehensive survival analytics for lane-changing duration, 2021, the 100th annual meeting of the transportation research board, Washington, DC.

5. Linbo Li, Yang Li(通讯), Daiheng Ni, Yue Zhang. Dynamic trajectory planning for automated lane-changing, 2021, the 100th annual meeting of the transportation research board, Washington, DC.

6. Linbo Li, Yang Li(通讯), Daiheng Ni. Incorporating human factors into LCM using fuzzy TCI model. 2021, the 100th annual meeting of the transportation research board, Washington, DC.

7. Linbo Li, Yang Li(通讯),Yahua Zhang. Study on Short-term Accurate Prediction of Parking Demand. 2020, the 99th annual meeting of the transportation research board, Washington, DC.


EI论文

1. 李林波, 李杨(通讯). 面向帕累托最优的换道轨迹规划[J].同济大学学报(自然科学版).（已录用）

2. 李林波, 李杨(通讯). 面向精细化管理的停车需求短时预测[J].同济大学学报(自然科学版),2021,49(09):1301-1306.

3. 李林波, 李杨(通讯),邹亚杰. 基于时依等比例风险回归模型的换道时长影响因素[J].同济大学学报(自然科学版),2021,49(07):933-940.

4. 李瑞杰, 李林波, 李杨, 邹亚杰. 跟驰模型场景基准分析[J].同济大学学报(自然科学版),2021,49(07):922-932+985.





