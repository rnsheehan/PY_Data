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

MOD_NAME_STR = "General"
HOME = False
USER = 'Robert' if HOME else 'robertsheehan/OneDrive - University College Cork/Documents'

def PDA10CS_Calibration():

    # plot the data obtained from the calibration of the PDA10CS power meter

    FUNC_NAME = ".PDA10CS_Calibration()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:        
        DATA_HOME = 'c:/users/robertsheehan/Programming/LabVIEW/Thorlabs_PDA10/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())
            #print(glob.glob('*.txt'))

            files = glob.glob('Cal_Swp_1_G_*.txt') + glob.glob('Cal_Swp_2_G_*.txt') + glob.glob('Cal_Swp_3_G_*.txt')

            print(files)

            # Read in the calibration data and make a plot
            IV_data = []; PV_data = []; marks = []; labels_mW = []; labels_V = []; 
            count = 0
            for i in range(0, len(files),1):
                data = numpy.loadtxt(files[i],delimiter = '\t',unpack = True)
                gval = 10*int(Common.extract_values_from_string(files[i])[1].replace('.',''))
                IV_data.append([data[0], data[1]]); 
                PV_data.append([data[1], data[2]]); 
                marks.append(Plotting.labs_pts[count%len(Plotting.labs_pts)])
                labels_mW.append('Swp %(v1)d'%{"v1":count})
                labels_V.append('Swp %(v1)d G = %(v2)d dB'%{"v1":count, "v2":gval})
                count = count + 1

            # Make the plot
            args = Plotting.plot_arg_multiple()

            args.loud = False
            args.crv_lab_list = labels_mW
            args.mrk_list = marks
            args.x_label = 'Current / mA'
            args.y_label = 'Power / mW'
            args.fig_name = 'OpticalPower_mW'
            #args.plt_range = [10, 80, 0, 5]

            Plotting.plot_multiple_curves(IV_data, args)

            args.loud = False
            args.crv_lab_list = labels_V
            args.mrk_list = marks
            args.x_label = 'Power / mW'
            args.y_label = 'Power / V'
            args.fig_name = 'OpticalPower_V'
            #args.plt_range = [10, 80, 0, 5]

            Plotting.plot_multiple_curves(PV_data, args)

            for i in range(0, len(files), 1):
                lin_fit = Common.linear_fit(PV_data[i][0], PV_data[i][1], [1,0.5])
                print(files[i],": ",lin_fit)

            IV_data.clear(); PV_data.clear(); labels_mW.clear(); labels_V.clear(); marks.clear();

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Diode_Fit_Calibration():

    # Using K2602 calibrate the Diode Equation Fitting Algorithms and the Ohm's Law Estimate of the diode series resistance
    # R. Sheehan 21 - 4 - 2022

    FUNC_NAME = ".Diode_Fit_Calibration()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Programming/LabVIEW/Keithley_2602/Diode_Fit_Test_Data/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            Rlist = ['000','010','022','047','067']
            file_template = 'FR1001_Rs_%(v1)s.txt'

            # plot all the measured data together
            hv_data = []; marks = []; labels = []; 
            count = 0
            for r in Rlist: 
                the_file = file_template%{"v1":r}
                if glob.glob(the_file):
                    data = numpy.loadtxt(the_file, delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append(Plotting.labs_pts[count%len(Plotting.labs_pts)])
                    labels.append('$R_{s}$  = %(v2)d $\Omega$'%{"v2":int(r)})
                    count = count + 1

            # Make the plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Current / mA'
            args.y_label = 'Voltage / V'
            args.fig_name = 'Measured_Data'
            args.plt_range = [0, 100, 0, 8]

            Plotting.plot_multiple_curves(hv_data, args)

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Sandbox():

    size_diff = -3
    print(numpy.zeros( abs(size_diff)  ))
    print(numpy.repeat( -1000, abs(size_diff)  ))