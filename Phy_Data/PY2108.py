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

MOD_NAME_STR = "PY2108"
HOME = False
USER = 'Robert' if HOME else 'robertsheehan/OneDrive - University College Cork/Documents'

def RC_FR_Plots():

    # Plot the measured Frequency Response Data for some RC circuits
    # R. Sheehan 13 - 5 - 2021

    FUNC_NAME = ".CE_AMP_IV_Char()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_SFMG_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 

        Rlist = [10, 46, 100]
        fname_tmplt = "FR_R_%(v1)d_C_2u.txt"
        for R in Rlist: 
            filename = fname_tmplt%{"v1":R}
            data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
            hv_data.append(data); labels.append("R = %(v1)d $\Omega$"%{"v1":R}); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );
            count = count + 1; 

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Frequency / kHz'
        args.y_label = 'Gain'
        args.fig_name = "RC_LPF_C_2u"
        args.plt_range = [0.5, 30, 0, 1]
        args.plt_title = "C = 0.22 $\mu$F"

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LRC_FR_Plots():

    # Plot the measured Frequency Response Data for some LRC circuits
    # R. Sheehan 13 - 5 - 2021

    FUNC_NAME = ".CE_AMP_IV_Char()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_SFMG_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 

        Llist = [100, 220]
        Clist = [100, 220]
        fname_tmplt = "RLC_R_10_L_%(v1)d_C_%(v2)dn.txt"
        for i in range(0, len(Llist), 1):
            for j in range(0, len(Clist), 1):
                filename = fname_tmplt%{"v1":Llist[i], "v2":Clist[j]}
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                hv_data.append(data); labels.append("L = %(v1)d $\mu$H, C = %(v2)d nF"%{"v1":Llist[i], "v2":Clist[j]}); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );
                count = count + 1; 

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Frequency / kHz'
        args.y_label = 'Gain'
        args.fig_name = "RLC_BPF_R_10"
        args.plt_range = [10, 80, 0, 1]
        args.plt_title = "R = 10 $\Omega$"

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)