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

    FUNC_NAME = ".RC_FR_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_SFMG_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 

        Rlist = [10, 46, 100, 1000]
        fname_tmplt = "FR_R_%(v1)d_C_2u_Alt_MCP602.txt"
        for R in Rlist: 
            filename = fname_tmplt%{"v1":R}
            data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
            scl = data[1][0]
            for i in range(0, len(data[1]), 1):
                data[1][i] = 10.0*math.log10( data[1][i] / scl )
            hv_data.append(data); labels.append("R = %(v1)d $\Omega$"%{"v1":R}); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );
            count = count + 1; 

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Frequency / kHz'
        args.y_label = 'Response / dB'
        args.fig_name = "RC_LPF_C_2u_Alt_MCP602"
        args.plt_range = [0.5, 30, -7, 1]
        args.plt_title = "C = 0.22 $\mu$F"

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def RC_FR_Compar_Plots():

    # Plot the measured Frequency Response Data for some RC circuits
    # R. Sheehan 13 - 5 - 2021

    FUNC_NAME = ".RC_FR_Compar_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_SFMG_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # import the data
        Rlist = [10, 46, 100, 1000]
        fname_tmplt = "FR_R_%(v1)d_C_2u%(v2)s"
        for R in Rlist: 
            hv_data = []; labels = []; marks = []; count = 0;
            
            filename = fname_tmplt%{"v1":R,"v2":".txt"}
            data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
            scl = data[1][0]
            for i in range(0, len(data[1]), 1):
                data[1][i] = 10.0*math.log10( data[1][i] / scl )
            hv_data.append(data); labels.append("SFMG"); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );

            count = count + 1;

            filename = fname_tmplt%{"v1":R,"v2":"_Alt_MCP602.txt"}
            data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
            scl = data[1][0]
            for i in range(0, len(data[1]), 1):
                data[1][i] = 10.0*math.log10( data[1][i] / scl )
            hv_data.append(data); labels.append("AD9833+MCP602"); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );

            count = count + 1; 

            # plot the data
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency / kHz'
            args.y_label = 'Response / dB'
            args.fig_name = "RC_LPF_C_2u_R_%(v1)d_MCP602"%{"v1":R}
            args.plt_range = [0.5, 30, -7, 1]
            args.plt_title = "C = 0.22 $\mu$F, R = %(v1)d $\Omega$"%{"v1":R}

            Plotting.plot_multiple_curves(hv_data, args)

            del args; del hv_data; del labels; del marks; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LRC_FR_Plots():

    # Plot the measured Frequency Response Data for some LRC circuits
    # R. Sheehan 13 - 5 - 2021

    FUNC_NAME = ".LRC_FR_Plots()" # use this in exception handling messages
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
        fname_tmplt = "RLC_R_10_L_%(v1)d_C_%(v2)dn_Alt_MCP6022.txt"
        for i in range(0, len(Llist), 1):
            for j in range(0, len(Clist), 1):
                filename = fname_tmplt%{"v1":Llist[i], "v2":Clist[j]}
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                scl = numpy.amax(data[1])
                for k in range(0, len(data[1]), 1):
                    data[1][k] = 10*math.log10( data[1][k] / scl )
                hv_data.append(data); labels.append("L = %(v1)d $\mu$H, C = %(v2)d nF"%{"v1":Llist[i], "v2":Clist[j]}); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );
                count = count + 1; 

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Frequency / kHz'
        args.y_label = 'Response / dB'
        args.fig_name = "RLC_BPF_R_10_Alt_MCP6022"
        args.plt_range = [10, 80, -6, 0]
        args.plt_title = "R = 10 $\Omega$"

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LRC_FR_Compar_Plots():

    # Plot the measured Frequency Response Data for some LRC circuits
    # R. Sheehan 13 - 5 - 2021

    FUNC_NAME = ".LRC_FR_Compar_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_SFMG_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # import the data     

        Llist = [100, 220]
        Clist = [100, 220]
        fname_tmplt = "RLC_R_10_L_%(v1)d_C_%(v2)dn%(v3)s"
        for i in range(0, len(Llist), 1):
            for j in range(0, len(Clist), 1):
                hv_data = []; labels = []; marks = []; 
                count = 0;

                filename = fname_tmplt%{"v1":Llist[i], "v2":Clist[j], "v3":".txt"}
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                scl = numpy.amax(data[1])
                for k in range(0, len(data[1]), 1):
                    data[1][k] = 10*math.log10( data[1][k] / scl )
                hv_data.append(data); labels.append("SFMG"); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );
                count = count + 1;
                
                filename = fname_tmplt%{"v1":Llist[i], "v2":Clist[j], "v3":"_Alt_MCP6022.txt"}
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                scl = numpy.amax(data[1])
                for k in range(0, len(data[1]), 1):
                    data[1][k] = 10*math.log10( data[1][k] / scl )
                hv_data.append(data); labels.append("AD9833+MCP6022"); marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] );
                count = count + 1;

                # plot the data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency / kHz'
                args.y_label = 'Response / dB'
                args.fig_name = "RLC_BPF_L_%(v1)d_C_%(v2)d_MCP6022"%{"v1":Llist[i], "v2":Clist[j]}
                args.plt_range = [10, 80, -6, 0]
                args.plt_title = "R = 10 $\Omega$, L = %(v1)d $\mu$H, C = %(v2)d nF"%{"v1":Llist[i], "v2":Clist[j]}

                Plotting.plot_multiple_curves(hv_data, args)

                del args; del hv_data; del labels; del marks; 

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)