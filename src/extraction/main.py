import  os
import argparse
from loguru import logger

from src.extraction.mergingExtraionClass import MergingExtracionClass

def createArgs():
    cs = argparse.ArgumentParser(description="Dataset Tracks Visualizer")

    cs.add_argument('--distance_threshold', default=200,
                    help="distance threshold to match the surrounding vehicles.", type=int)

    cs.add_argument('--lookback', default=3,
                    help="this variable is set is to ensure the accuracy of the extracted trajectory.",
                    type=int)

    cs.add_argument('--timestep', default=0.04,
                    help="recording frequency.",
                    type=int)

    return vars(cs.parse_args())

def main():

    config = createArgs()
    logger.info("Extracting trajectories and calculating metrics")
    logger.info("distance threshold {}, lookback is {}",config["distance_threshold"],config["lookback"])


    trajectoryExtraction = MergingExtracionClass(config)
    trajectoryExtraction.run()

if __name__ == '__main__':
    main()

