import sys
import os 
import glob
import re

import math
import scipy
import numpy
import matplotlib.pyplot as plt

import Common
import Plotting
import SpctrmPlt

MOD_NAME_STR = "LLM"
HOME = False
USER = 'Robert' if HOME else 'robertsheehan/OneDrive - University College Cork/Documents'

def JDSU_EDFA_Plot():

    # generate a plot of the measured JDSU laser spectrum data
    # R. Sheehan 21 - 9 - 2021

    FUNC_NAME = ".JDSU_EDFA_Plot()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/JDSU_DFB_EDFA/'

        if os.path.isdir(dir_name):

            file_names = ['JDSU_DFB_Only.txt', 'FP_EDFA_Gain.txt', 'JDSU_DFB_Amp.txt']

            os.chdir(dir_name)
            print("Current Directory: ")
            print(os.getcwd())

            #data = numpy.loadtxt(file_names[0], delimiter = ',', skiprows = 3, unpack = True, max_rows = 5001)

            labels = ['JDSU DFB', 'EDFA', 'JDSU + EDFA']
            plot_range = [1550, 1560, -70, 20]
            plt_title = ''
            plt_name = 'JDSU_Amp'

            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, labels, plot_range, plt_title, plt_name, loudness = True)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
