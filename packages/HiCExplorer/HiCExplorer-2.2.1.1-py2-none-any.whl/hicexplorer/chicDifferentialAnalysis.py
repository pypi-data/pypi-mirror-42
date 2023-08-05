# read background model
# read file 1
#read file 2
import argparse
import sys
import numpy as np
from hicmatrix import HiCMatrix as hm
# from hicexplorer.utilities import toString
from hicexplorer._version import __version__
from .lib import Viewpoint
from .lib import Utilities

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import os

import math
import logging
log = logging.getLogger(__name__)


def parse_arguments(args=None):
    parser = argparse.ArgumentParser(add_help=False,
                                     description='Plots the number of interactions around a given reference point in a region.')

    parserRequired = parser.add_argument_group('Required arguments')

    parserRequired.add_argument('--interactionFile', '-if',
                                help='path to the interaction files which should be used for plotting',
                                required=True)
    parserRequired.add_argument('--interactionFileWildType', '-ifwt',
                                help='path to the interaction files which should be used for plotting',
                                required=True)

    parserRequired.add_argument('--backgroundModelFile', '-bmf',
                           help='path to the background file which should be used for plotting',
                           required=False)
    
    parserRequired.add_argument('--outFileName', '-o',
                                help='File name to save the result.',
                                required=True)

    parserOpt = parser.add_argument_group('Optional arguments')



    parserOpt.add_argument('--range',
                           help='Defines the region upstream and downstream of a reference point which should be included. '
                           'Format is --region upstream downstream',
                           required=False,
                           type=int,
                           nargs=2)
    parserOpt.add_argument('--threshold',
                           help='Upper and lower threshold for rbz-score',
                           required=False,
                           type=int,
                           nargs=2)

    parserOpt.add_argument("--help", "-h", action="help", help="show this help message and exit")

    parserOpt.add_argument('--version', action='version',
                           version='%(prog)s {}'.format(__version__))
    return parser


def main(args=None):
    args = parse_arguments().parse_args(args)
    viewpointObj = Viewpoint()
    # utilitiesObj = Utilities()
    # background_data = None
    # background_data_sorted = None

    background_data = viewpointObj.readBackgroundDataFile(args.backgroundModelFile)

    backgroundModelData, backgroundModelSEM = viewpointObj.interactionBackgroundData(background_data, args.range)
    _, interaction_data, rbz_score, _ = viewpointObj.readInteractionFile(args.interactionFile, args.range)
    _, interaction_data_wt, rbz_score_wt, _ = viewpointObj.readInteractionFile(args.interactionFileWildType, args.range)

    log.debug('length interaction_data {}'.format(len(interaction_data)))
    interaction_data_np = np.empty(len(interaction_data))
    interaction_data_wt_np = np.empty(len(interaction_data_wt))
    rbz_score_np = np.empty(len(rbz_score))
    for i, key in enumerate(sorted(interaction_data)):
        interaction_data_np[i] = interaction_data[key]

    for i, key in enumerate(sorted(interaction_data_wt)):
        interaction_data_wt_np[i] = interaction_data_wt[key]
    
    for i, key in enumerate(sorted(rbz_score)):
        rbz_score_np[i] = rbz_score[key]

    ## get all values which are greater than the background model as candidates
    log.debug('interaction_data_np {}'.format(interaction_data_np))
    log.debug('interaction_data_wt_np {}'.format(interaction_data_wt_np))
    log.debug('rbzscore_np {}'.format(rbz_score_np))
    

    # candidates = interaction_data_np > backgroundModelData

    _candidates_rbz_score_lower = rbz_score_np > args.threshold[0]
    _candidates_rbz_score_upper = rbz_score_np < args.threshold[1]
    candidates_rbz_score = np.logical_and(_candidates_rbz_score_lower, _candidates_rbz_score_upper)

    log.debug('candidates_rbz_score {}'.format(candidates_rbz_score))
    
    