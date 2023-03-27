# A-reproducible-approach-to-merging-behavior-analysis-based-on-High-Definition-Map

**My personal website: www.vehicletrajectorymining.com.**

## About
This project contains the source code and data for the paper titled "A reproducible approach to merging behavior analysis based on High Definition Map".

### Citation
```
@article{
    Yang Li, 2023
    "https://arxiv.org/abs/2303.11531"
    title={A reproducible approach to merging behavior analysis based on High Definition Map}, 
    author={Yang Li and Yang Liu and Daiheng Ni and Ang Ji and Linbo Li and Yajie Zou},
    year={2023},
    eprint={2303.11531},
    archivePrefix={arXiv},
    primaryClass={cs.RO}
}
```

### Code Structure

```
A reproducible approach to merging behavior analysis based on High Definition Map/
|__ asset: analysis results
|    |__ acceptedGaps
|    |__ backgroundPicture
|    |__ consecutiveLaneChange
|    |__ JSDivergence
|    |__ preliminaryAnalysis
|    |__ safetyAnalysis
|    |__ table
|    |__ trafficFlowSpeed
|__ conf: experiment configurations
|    |__ lanelet2map
|__ drone-dataset-tools-master: dataset
|__ src: merging trajectories extraction, indicators calculation, results visulization
|    |__ extraction
|    |__ figure
|    |    |__accepetedGapAnalysis
|    |    |__consecutiveLanechangeAnalysis
|    |    |__preliminaryAnalysis
|    |    |__safetyAnalysis
|    |    |__similarityAnalysis
|    |    |__trafficFlowSpeedDensity
|    |__ table
|__ utils: utility functions
|__ requirements.txt: required packages
```


**Abstract:**
Existing research on merging behavior generally prioritize the application of various algorithms, but often overlooks the fine-grained process and analysis of trajectories. This leads to the neglect of surrounding vehicle matching, the opaqueness of indicators definition, and reproducible crisis. To address these gaps, this paper presents a reproducible approach to merging behavior analysis. Specifically, we outline the causes of subjectivity and irreproducibility in existing studies. Thereafter, we employ lanelet2 High Definition (HD) map to construct a reproducible framework, that minimizes subjectivities, defines standardized indicators, identifies alongside vehicles, and divides scenarios. A comparative macroscopic and microscopic analysis is subsequently conducted. More importantly, this paper adheres to the Reproducible Research concept, providing all the source codes and reproduction instructions. Our results demonstrate that although scenarios with alongside vehicles occur in less than 6% of cases, their characteristics are significantly different from others, and these scenarios are often accompanied by high risk. This paper refines the understanding of merging behavior, raises awareness of reproducible studies, and serves as a watershed moment.

**Keywords:**
Merging Behavior, High Definition Map, Reproducible Research, exiD dataset.

**Research bullets**
1. Merging distance
2. Merging distance ratio
3. Merging duration
4. Merging lateral trajectory
5. Merging lateral speed
6. Scenario classification
7. Alongside vehicle identification
8. HD map pre-labeling
9. Standardized indicators
10. Safety analysis
11. Traffic flow-density-speed
12. Accepted gap analysis
13. Scenario similarity
14. Consecutive lane-changing duration


## Install

1. Create new conda environment
You are recommended to create a new Conda environment to install the project
```bash
conda create -n MBA python=3.7
conda activate MBA
```

2. Clone this repo

```bash
git clone https://github.com/iyangli/A-reproducible-approach-to-merging-behavior-analysis-based-on-High-Definition-Map.git
```

3. Install all required packages
```bash
pip install -r requirements.txt
```

## Usage




## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## Developers
Yang Li ( yangli.chn@outlook.com )

For help or issues using the code, please create an issue for this repository or contact Yang Li ( yangli.chn@outlook.com ).


## Contact

For general questions about the paper, please contact Yang Li ( yangli.chn@outlook.com ).

