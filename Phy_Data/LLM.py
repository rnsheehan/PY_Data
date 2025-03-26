from ast import Try
import sys
import os 

import glob
import re
#import ctypes # need this to access DLLs
#import ctypes.util
import subprocess

import math
import scipy
import numpy
import matplotlib.pyplot as plt

import pandas
import pprint

import copy

import Common
import Plotting
import SpctrmPlt

MOD_NAME_STR = "LLM"
HOME = False
USER = 'Robert' if HOME else 'robertsheehan/OneDrive - University College Cork/Documents'

def JDSU_DFB_LIV():

    # plot the measured JDSU DFB LIV data
    # R. Sheehan 14 - 10 - 2021

    FUNC_NAME = ".JDSU_DFB_LIV()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/JDSU_DFB_EDFA/'
        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Data/DFB_Char/'

        if os.path.isdir(dir_name):
            os.chdir(dir_name)
            print(os.getcwd())

            LIV_plot = True

            if LIV_plot:

                files = glob.glob('JDSU_CQF915_508_T_*_PM100D_S155C.txt')

                # Plot the measured LIV data            
                hv_data_v = []; hv_data_mW = []; hv_data_dBm = []; marks = []; labels = []; 
                Tvals = [20, 23, 25, 27, 30, 33, 35]
                for i in range(0, len(files), 1):
                    labels.append("T = %(v1)d C"%{"v1":Tvals[i]})
                    marks.append( Plotting.labs_lins[ i % ( len( Plotting.labs_lins ) ) ] )
                    data = numpy.loadtxt(files[ i ], delimiter = '\t', unpack = True)
                    hv_data_v.append([data[0], data[1]])
                    hv_data_mW.append([data[0], data[2]])
                    hv_data_dBm.append([data[0], data[3]])

                # plot the data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = r'$I_{DFB}$ / mA'
                args.y_label = r'$V_{DFB}$ / V'
                args.fig_name = 'JDSU_CQF915_508_Voltage'
                #args.plt_range = [0, 50, 0, 1.1]

                Plotting.plot_multiple_curves(hv_data_v, args)

                args.y_label = r'$P_{DFB}$ / mW'
                args.fig_name = 'JDSU_CQF915_508_PmW'
                #args.plt_range = [0, 50, 0, 7]

                Plotting.plot_multiple_curves(hv_data_mW, args)

                args.y_label = r'$P_{DFB}$ / dBm'
                args.fig_name = 'JDSU_CQF915_508_PdBm'
                #args.plt_range = [0, 50, -40, 10]

                Plotting.plot_multiple_curves(hv_data_dBm, args)

                del hv_data_v; del hv_data_mW; del hv_data_dBm;

                # Plot the peak voltage, power as function of temperature
                #Tvals = []
                Vpeak = []
                Ppeak = []
                for i in range(0, len(files), 1):
                    #Tvals.append( float( files[ i ].replace('DFB_LIV_T','').replace('.txt','').replace('_','') ) )
                    data = numpy.loadtxt(files[ i ], delimiter = '\t', unpack = True)
                    Vpeak.append(data[1][-1])
                    Ppeak.append(data[2][-1])

                # Linear fit the Peak power versus Temperature
                Common.linear_fit(numpy.asarray(Tvals), numpy.asarray(Ppeak), [1, 1], True)
                # intercept = 10.165010586385849 mW
                # slope = -0.06307007753890415 mW / K

                # plot the data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = r'$T_{DFB}$ / C'
                args.y_label = r'$V_{DFB}$ / V'
                args.y_label_2 = r'$P_{DFB}$ / mW'
                args.fig_name = 'JDSU_CQF915_508_I_200'
                args.plt_title = 'JDSU CQF915/508 $I_{DFB}$ = 200 mA'
            
                Plotting.plot_two_axis(Tvals, Vpeak, Ppeak, args) 
                
                del Tvals; del Vpeak; del Ppeak; del args; 
            
            # plot the optical spectra as function of temperature
            SPCTR_plot = False

            if SPCTR_plot:
                files = glob.glob('JDSU_CQF915_508_T*I_100_Spctrm.txt')

                # Plot the measured LIV data            
                hv_data = []; marks = []; labels = []; WL_max = []; P_max = []; 
                Tvals = [20, 23, 25, 27, 30, 33, 35]
                for i in range(0, len(files), 1):
                    labels.append("T = %(v1)d C"%{"v1":Tvals[i]})
                    marks.append( Plotting.labs_lins[ i % ( len( Plotting.labs_lins ) ) ] )
                    data = numpy.loadtxt(files[ i ], delimiter = '\t', unpack = True)
                    WL_max.append(data[0][numpy.argmax(data[1])] )
                    P_max.append(numpy.max(data[1]))
                    hv_data.append([data[0], data[1]])

                # plot the data
                OSA_plot = False
                if OSA_plot:
                    args = Plotting.plot_arg_multiple()

                    args.loud = True
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = r'Wavelength $\lambda$ / nm'
                    args.y_label = 'Power dBm / 0.05nm'
                    args.fig_name = 'JDSU_CQF915_508_Spectrum'
                    args.plt_title = 'JDSU CQF915/508 $I_{DFB}$ = 100 mA'
                    #args.plt_range = [0, 50, 0, 1.1]

                    Plotting.plot_multiple_curves(hv_data, args)

                WLT_plot = True
                if WLT_plot:

                    # linear fits to the peak WL versus T data
                    Common.linear_fit(numpy.asarray(Tvals), numpy.asarray(WL_max), [1, 1], True)
                    # slope: 0.09424227543241155 nm / K
                    # intercept: 1547.0581772630778 nm

                    args = Plotting.plot_arg_multiple()

                    args.loud = True
                    args.x_label = r'$T_{DFB}$ / C'
                    args.y_label = r'$\lambda_{peak}$ / nm'
                    args.y_label_2 = r'$P_{peak}$ / dBm / 0.05 nm'
                    args.fig_name = 'JDSU_CQF915_508_I_100'
                    #args.plt_title = 'JDSU CQF915/508 $I_{DFB}$ = I00 mA'
            
                    Plotting.plot_two_axis(Tvals, WL_max, P_max, args) 

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def JDSU_EDFA_Plot():

    # generate a plot of the measured JDSU laser spectrum data after amplification with EDFA
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
            plot_range = [1550, 1560, -80, 20]
            plt_title = ''
            plt_name = 'JDSU_Amp'

            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, labels, plot_range, plt_title, plt_name, loudness = True)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def JDSU_Filter_Plot():

    # generate a plot of the measured JDSU laser spectrum data after passing through Santec Filter
    # R. Sheehan 21 - 9 - 2021

    FUNC_NAME = ".JDSU_Filter_Plot()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/JDSU_DFB_EDFA/'

        if os.path.isdir(dir_name):

            file_names = ['JDSU_DFB_Again.txt', 'JDSU_Filtered.txt']

            os.chdir(dir_name)
            print("Current Directory: ")
            print(os.getcwd())

            #data = numpy.loadtxt(file_names[0], delimiter = ',', skiprows = 3, unpack = True, max_rows = 5001)

            labels = ['JDSU DFB', 'JDSU Filtered']
            plot_range = [1550, 1560, -80, 20]
            plt_title = ''
            plt_name = 'JDSU_Filt'

            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, labels, plot_range, plt_title, plt_name, loudness = True)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def JDSU_Isolator_Plot():

    # generate a plot of the measured JDSU laser spectrum data after passing through Isolator
    # R. Sheehan 6 - 10 - 2021

    FUNC_NAME = ".JDSU_Isolator_Plot()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/JDSU_DFB_EDFA/'

        if os.path.isdir(dir_name):

            file_names = ['JDSU_DFB_Only_2.txt', 'JDSU_DFB_Iso.txt', 'JDSU_DFB_Iso_Return.txt']

            os.chdir(dir_name)
            print("Current Directory: ")
            print(os.getcwd())

            #data = numpy.loadtxt(file_names[0], delimiter = ',', skiprows = 3, unpack = True, max_rows = 5001)

            labels = ['JDSU DFB', 'JDSU Isolator', 'Isolator Return']
            plot_range = [1550, 1560, -85, 5]
            plt_title = ''
            plt_name = 'JDSU_Iso'

            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, labels, plot_range, plt_title, plt_name, loudness = True)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def JDSU_Only():

    # generate a plot of the measured JDSU laser spectrum
    # R. Sheehan 6 - 10 - 2021

    FUNC_NAME = ".JDSU_Isolator_Plot()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/JDSU_DFB_EDFA/'

        if os.path.isdir(dir_name):

            file_names = ['JDSU_DFB_Only.txt']

            os.chdir(dir_name)
            print("Current Directory: ")
            print(os.getcwd())

            #data = numpy.loadtxt(file_names[0], delimiter = ',', skiprows = 3, unpack = True, max_rows = 5001)

            labels = ['JDSU DFB']
            plot_range = [1550, 1560, -70, 5]
            plt_title = ''
            plt_name = 'JDSU_Only'

            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, labels, plot_range, plt_title, plt_name, loudness = True)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LLM_Setup():

    FUNC_NAME = ".LLM_Setup()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:

        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/DSHI_LLM_Setup_Test/'

        if os.path.isdir(dir_name):
            
            os.chdir(dir_name)
            print("Current Directory: ")
            print(os.getcwd())

            files = glob.glob("W*.txt")
            labels = ['LLM Input', 'Coupler 1', 'Coupler 2', 'After Link', 'After EDFA', 'After Filter', 'After VOA', 'After PC', 'After AOM', 'LLM Output']
            plot_range = [1550, 1560, -85, 15]
            plt_title = ''
           
            #for i in range(0, len(files), 1):
            #    file_names = [files[i]]
            #    label_list = [labels[i]]
            #    plt_name = labels[i]

            #    SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = False)

            file_names = ['W0000.txt', 'W0001.txt', 'W0002.txt']
            label_list = ['LLM Input', 'Coupler 1', 'Coupler 2']
            plt_name = 'LLM Input'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0000.txt', 'W0002.txt', 'W0003.txt']
            label_list = ['LLM Input', 'Coupler 2', 'D = 25 km']
            plt_name = 'LLM After Link'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0002.txt', 'W0003.txt', 'W0004.txt']
            label_list = ['Coupler 2', 'D = 25 km', 'After EDFA']
            plt_name = 'Amp After Link'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0002.txt', 'W0003.txt', 'W0004.txt', 'W0005.txt']
            label_list = ['Coupler 2', 'D = 25 km', 'After EDFA', 'After Filter']
            plt_name = 'Filter After Link'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0002.txt', 'W0003.txt', 'W0004.txt', 'W0006.txt']
            label_list = ['Coupler 2', 'D = 25 km', 'After EDFA', 'After VOA']
            plt_name = 'VOA After Link'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0002.txt', 'W0003.txt', 'W0004.txt', 'W0007.txt']
            label_list = ['Coupler 2', 'D = 25 km', 'After EDFA', 'After PC']
            plt_name = 'PC After Link'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0000.txt', 'W0001.txt', 'W0008.txt']
            label_list = ['LLM Input', 'Coupler 1', 'After AOM']
            plt_name = 'LLM After AOM'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0008.txt', 'W0007.txt', 'W0009.txt']
            label_list = ['After AOM', 'After PC', 'DSHI Output']
            plt_name = 'LLM After DSHI'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

            file_names = ['W0000.txt', 'W0009.txt']
            label_list = ['LLM Input', 'DSHI Output']
            plt_name = 'LLM IO'
            SpctrmPlt.multiple_optical_spectrum_plot(dir_name, file_names, label_list, plot_range, plt_title, plt_name, loudness = True)

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LLM_Sample_Data():

    # make plots of the measured LLM sample data that you found
    # R. Sheehan 20 - 10 - 2021

    FUNC_NAME = ".LLM_Sample_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Lorentzian_Analysis/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            # Get the data
            files = ['Sample_LLM.txt']
            #files = ['Sample_LLM.txt', 'Lorentz_fin1.csv', 'Lorentz_fin2.csv', 'Lorentz_draft.csv', 'Lorentz_iodeal.csv', 'Voigt_draft.csv', 'Voigt_fin1.csv']
            for i in range(0, len(files), 1):
                hv_data = []; labels = []; marks = []; 
                data = numpy.loadtxt(files[i], skiprows = 1, unpack = True)
                #data = numpy.loadtxt(files[i], delimiter = ',', skiprows = 1, unpack = True)
                data[0] = data[0] / 1.0e+3; 
                data[2] = data[2] / 1.0e+3; 
                hv_data.append([data[0], data[1]]); labels.append('Raw Data'); marks.append(Plotting.labs_pts[2]); 
                hv_data.append([data[2], data[3]]); labels.append('Lor Fit'); marks.append(Plotting.labs_lins[0]); 

                # plot the data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency / MHz'
                args.y_label = 'Spectral Power / dBm'
                args.fig_name = files[i].replace('.txt','')
                #args.plt_range = [0, 3.3, 0, 140]

                Plotting.plot_multiple_curves(hv_data, args)

                hv_data.clear(); labels.clear(); marks.clear(); 
        else:
            raise EnvironmentError
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Spectra_vs_Current():

    # make plot of measured spectra at different laser current values
    # R. Sheehan 18 - 11 - 2021

    FUNC_NAME = ".Spectra_vs_Current()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/'

        method = 'DSHI'
        laser = 'JDSU_DFB'
        temperature = '20'
        dlength = '25'

        dir_name = '%(v1)s_%(v2)s_T_%(v3)s_D_%(v4)s/'%{"v1":method, "v2":laser, "v3":temperature, "v4":dlength}

        new_dir = DATA_HOME + dir_name

        if os.path.isdir(new_dir):
            os.chdir(new_dir)

            print(os.getcwd())

            fname = 'LLM_Spctrm_I_%(v1)d.txt'
            Ivals = list(range(40, 60, 5))

            # import the measured data
            hv_data = []; marks = []; labels = []
            count = 0
            for x in Ivals:
                filename = fname%{"v1":x}
                if glob.glob(filename):
                    data = numpy.loadtxt(filename, unpack = True)
                    hv_data.append(data); 
                    marks.append(Plotting.labs_lins[count%len(Plotting.labs_lins)]);
                    labels.append( 'I = %(v1)d mA'%{"v1":x} )
                    count = count + 1
            
            # make the plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency / MHz'
            args.y_label = 'Spectral Power / dBm'
            args.fig_name = dir_name.replace('/','_') + 'Spectra'
            args.plt_range = [65, 95, -80, -50]

            Plotting.plot_multiple_curves(hv_data, args)

            hv_data.clear(); labels.clear(); marks.clear(); 
            
        else:
            raise EnvironmentError

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Meas_Report():

    # plot the measured LLM versus time for each file
    # R. Sheehan 18 - 11 - 2021

    FUNC_NAME = ".Meas_Report()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_Setup_Test/'

        # Enter the values below
        method = 'LCR_DSHI' # LLM Method
        laser = 'JDSU_DFB' # laser name / type
        temperature = '20' # laser temperature
        dlength = '50' # fibre loop length
        
        dir_name = '%(v1)s_%(v2)s_T_%(v3)s_D_%(v4)s/'%{"v1":method, "v2":laser, "v3":temperature, "v4":dlength}

        new_dir = DATA_HOME + dir_name

        if os.path.isdir(new_dir):
            os.chdir(new_dir)

            print(os.getcwd())

            filename = glob.glob('LLM_Data_Nmeas_100*.txt')

            LL_Vfit = 7; LL_Vfit_Rsqr = 15; 
            LL_Lfit = 8; LL_Lfit_Rsqr = 22; 

            for f in filename: Meas_Analysis(f, LL_Vfit, LL_Vfit_Rsqr)

            
        else:
            raise EnvironmentError

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Meas_Analysis(filename, LL_col, LL_col_Rsqr):

    # Read in the file containing the data from the Multi-LLM Meas
    # file has rows of data in the form 
    # {Time/s [0],	Tair/C [1],	Taom/s [2],	Taomdrv/s [3],	Pmax/dBm [4],	Fmax/MHz [5],	LLest/MHz [6],	LL_Vfit/MHz [7],	LL_Lfit/MHz [8],	Voigt_h/nW [9],	Voigt_c/MHz [10],	
    # Voigt_Lor_HWHM/MHz [11],	Voigt_Gau_Stdev/MHz	[12], Voigt_chisqr [13],	Voigt_chisqr_nu [14],	Voigt_Rsqr [15],	Voigt_gof [16],	Lor_h/nW [17],	Lor_c/MHz [18],	Lor_HWHM/MHz [19],
    # 	Lor_chisqr [20],	Lor_chisqr_nu [21],	Lor_Rsqr [22],	Lor_gof [23]}
    # Mainly interested in getting average LLM + error and also to see if there is zero correlation between LLM and time
    # R. Sheehan 7 - 1 - 2022

    FUNC_NAME = ".Meas_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:        
        if glob.glob(filename):

            from scipy.stats import kurtosis # use this to compute Kurtosis of measured LLM
            # https://en.wikipedia.org/wiki/Kurtosis
            # usual interpretation is Person's kurtosis K = 3 => normal distribution
            # Fisher's kurtosis K - 3 => 0 => normal distribution
            # K < 3 => platykurtic => distribution produces fewer and less extreme outliers than does the normal distribution
            # K > 3 => leptokurtic => distribution produces more extreme outliers than does the normal distribution

            data = numpy.loadtxt(filename, comments = '#', unpack = True)

            time_col = 0; 

            # get average LL + error
            LLave = numpy.mean(data[LL_col])
            LLstd = numpy.std(data[LL_col], ddof = 1)
            LLspread = 0.5*(numpy.max(data[LL_col]) - numpy.min(data[LL_col]))

            # get average R^{2} + error
            Rave = numpy.mean(data[LL_col_Rsqr])
            Rstd = numpy.std(data[LL_col_Rsqr], ddof = 1)
            Rspread = 0.5*(numpy.max(data[LL_col_Rsqr]) - numpy.min(data[LL_col_Rsqr]))

            # get correlation between measured LLM and time data
            # ideally this should be zero
            LLrcoeff = numpy.corrcoef(data[time_col], data[LL_col])

            # compute the distribution Kurtosis
            KK = kurtosis(data[LL_col], fisher = False)

            # compute the distribution Kurtosis
            KKR = kurtosis(data[LL_col_Rsqr], fisher = False)

            print(filename)
            print('Laser Linewidth: ',LLave,' +/-',LLspread,' MHz')
            print('Laser Linewidth: ',LLave,' +/-',LLstd,' MHz')
            print('Laser Linewidth vs Time Correlation Coefficient: ', LLrcoeff[1][0])
            print('Laser Linewidth vs Time Correlation Coefficient: ', LLrcoeff[0][1])
            print('Kurtosis of data: ', KK)

            # Plot LLM vs Time
            args = Plotting.plot_arg_single()

            args.loud = False
            args.x_label = 'Time / min'
            args.y_label = r'$\Delta \\nu$ / MHz'
            args.plt_title = r'<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, r = %(v3)0.3f'%{"v1":LLave,"v2":LLstd, "v3":LLrcoeff[0][1]}
            args.fig_name = filename.replace('.txt','_') + 'LLMvsTime'
            #args.plt_range = [0, 60, 1, 2]

            Plotting.plot_single_linear_fit_curve(data[time_col]/60.0, data[LL_col], args)

            # Plot histogram of LLM data
            
            args.x_label = 'Laser Linewidth / MHz'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram'
            args.plt_title = r'<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":LLave,"v2":LLstd, "v3":KK}

            Plotting.plot_histogram(data[LL_col], args)

            args.x_label = 'Lorentzian Fit $R^{2}$ coefficient'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram_Rsqr'
            args.plt_title = r'$R^{2}$ = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":Rave,"v2":Rstd, "v3":KKR}

            Plotting.plot_histogram(data[LL_col_Rsqr], args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open' + filename
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Meas_Analysis_Old(filename):

    # Read in the file containing the data from the Multi-LLM Meas
    # file has rows of data in the form {time / s, fitted A / nW, fitted f_centre / MHz, fitted LL / MHz, chi^{2} / nu for fit, R^{2} coeff, gof probablity}
    # Mainly interested in getting average LLM + error and also to see if there is zero correlation between LLM and time
    # R. Sheehan 18 - 11 - 2021

    FUNC_NAME = ".Meas_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:        
        if glob.glob(filename):

            from scipy.stats import kurtosis # use this to compute Kurtosis of measured LLM
            # https://en.wikipedia.org/wiki/Kurtosis
            # usual interpretation is Person's kurtosis K = 3 => normal distribution
            # Fisher's kurtosis K - 3 => 0 => normal distribution
            # K < 3 => platykurtic => distribution produces fewer and less extreme outliers than does the normal distribution
            # K > 3 => leptokurtic => distribution produces more extreme outliers than does the normal distribution

            data = numpy.loadtxt(filename, unpack = True)

            # get average LL + error
            LLave = numpy.mean(data[3])
            LLstd = numpy.std(data[3], ddof = 1)
            LLspread = 0.5*(numpy.max(data[3]) - numpy.min(data[3]))

            # get average R^{2} + error
            Rave = numpy.mean(data[5])
            Rstd = numpy.std(data[5], ddof = 1)
            Rspread = 0.5*(numpy.max(data[5]) - numpy.min(data[5]))

            # get correlation between measured LLM and time data
            # ideally this should be zero
            LLrcoeff = numpy.corrcoef(data[0], data[3])

            # compute the distribution Kurtosis
            KK = kurtosis(data[3], fisher = False)

            # compute the distribution Kurtosis
            KKR = kurtosis(data[5], fisher = False)

            print(filename)
            print('Laser Linewidth: ',LLave,' +/-',LLspread,' MHz')
            print('Laser Linewidth: ',LLave,' +/-',LLstd,' MHz')
            print('Laser Linewidth vs Time Correlation Coefficient: ', LLrcoeff[1][0])
            print('Laser Linewidth vs Time Correlation Coefficient: ', LLrcoeff[0][1])
            print('Kurtosis of data: ', KK)

            # Plot LLM vs Time
            args = Plotting.plot_arg_single()

            args.loud = False
            args.x_label = 'Time / min'
            args.y_label = r'$\Delta \\nu$ / MHz'
            args.plt_title = r'<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, r = %(v3)0.3f'%{"v1":LLave,"v2":LLspread, "v3":LLrcoeff[0][1]}
            args.fig_name = filename.replace('.txt','_') + 'LLMvsTime'
            args.plt_range = [0, 60, 1, 2]

            Plotting.plot_single_linear_fit_curve(data[0]/60.0, data[3], args)

            # Plot histogram of LLM data
            
            args.x_label = 'Laser Linewidth / MHz'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram'
            args.plt_title = r'<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":LLave,"v2":LLspread, "v3":KK}

            Plotting.plot_histogram(data[3], args)

            args.x_label = 'Lorentzian Fit $R^{2}$ coefficient'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram_Rsqr'
            args.plt_title = r'$R^{2}$ = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":Rave,"v2":Rspread, "v3":KKR}

            Plotting.plot_histogram(data[5], args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open' + filename
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LL_Result():

    # Plot the measured LL for various powers
    # R. Sheehan 18 - 11 - 2021

    FUNC_NAME = ".LL_Result()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/'

        method = 'DSHI'
        laser = 'JDSU_DFB'
        temperature = '20'
        dlength = '25'

        dir_name = '%(v1)s_%(v2)s_T_%(v3)s_D_%(v4)s/'%{"v1":method, "v2":laser, "v3":temperature, "v4":dlength}

        new_dir = DATA_HOME + dir_name

        if os.path.isdir(new_dir):
            
            current_mA = [40, 45, 50, 50, 50, 55, 60, 65]
            power_mW = [4.4748, 5.2278, 5.9808, 5.9808, 5.9808, 6.7338, 7.4868, 8.2398]
            ll_MHz = [1.55, 1.53, 1.21, 1.26, 1.30, 1.24, 1.16, 1.12]
            dll_MHz = [0.17, 0.29, 0.05, 0.10, 0.15, 0.11, 0.06, 0.06]

            power_inverse = []
            for i in range(0, len(power_mW), 1):
                power_inverse.append(1.0/power_mW[i])

            # Plot LLM vs Time
            args = Plotting.plot_arg_single()

            args.loud = True
            args.x_label = r'Inverse Power $P^{-1}$ / mW$^{-1}$'
            args.y_label = r'Laser Linewidth $\Delta \\nu$ / MHz'
            #args.plt_title = r'<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz'%{"v1":LLave,"v2":LLspread}
            args.fig_name = 'JDSU_DFB_Laser_Linewidth_D_25'
            args.plt_range = [0.1, 0.25, 1, 2]

            #Plotting.plot_single_linear_fit_curve(power_inverse, ll_MHz, args)
            Plotting.plot_single_linear_fit_curve_with_errors(power_inverse, ll_MHz, dll_MHz, args)

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LL_Result_Voigt():

    # Plot the measured LL for various powers
    # R. Sheehan 18 - 11 - 2021

    FUNC_NAME = ".LL_Result()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/'

        
        dir_name = 'Sample_Data'

        new_dir = DATA_HOME + dir_name

        if os.path.isdir(new_dir):

            os.chdir(new_dir)
            
            current_mA = [40, 45, 50, 55, 60, 65]
            power_mW = [4.4748, 5.2278, 5.9808, 6.7338, 7.4868, 8.2398]
            ll_MHz = [2.16, 2.2, 2.23, 2.29, 2.39, 2.45]

            power_inverse = []
            for i in range(0, len(power_mW), 1):
                power_inverse.append(1.0/power_mW[i])

            # Plot LLM vs Time
            args = Plotting.plot_arg_single()

            args.loud = True
            args.x_label = r'Inverse Power $P^{-1}$ / mW$^{-1}$'
            args.y_label = r'Laser Linewidth $\Delta \\nu$ / MHz'
            #args.plt_title = r'<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz'%{"v1":LLave,"v2":LLspread}
            args.fig_name = 'JDSU_DFB_Laser_Linewidth_D_25_Power'
            #args.plt_range = [0.1, 0.25, 1, 2]

            Plotting.plot_single_linear_fit_curve(power_inverse, ll_MHz, args)
            #Plotting.plot_single_linear_fit_curve_with_errors(power_inverse, ll_MHz, dll_MHz, args)

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Lorentz_Voigt_Fit_Analysis():

    # make plots of the Lorentz and Voigt fits to the sample data sets
    # Data is stored in rows of the files in the form
    # row 0: freq fit data, row 1: LLM spctrl data, row 2: Voigt f vals, row 3: Voigt resids, row 4: Lorentz f vals, row 5: Lorentz f resids
    # R. Sheehan 13 - 12 - 2021

    FUNC_NAME = ".Lorentz_Voigt_Fit_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Sample_Data/'
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/NKT_LCR_DSHI/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            #Vvals = ['000','100','200','300','325','350','360','365','370','375','400']
            #Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]
            Vvolts = numpy.arange(80, 2965, 80)

            #filetmplt = 'JDSU_DFB_T_20_I_50_V_%(v1)s_fit_results.txt'
            filetmplt = 'NKT_I_100_Vb_30_RBW_05_fb_%(v1)d_fit_results.txt'

            CONVERT_TO_dBm = True

            scale_factor = 1.0e+6
            nfiles = 12
            for i in range(0, len(Vvolts), 1):
                #file_tmplt = 'Smpl_LLM_%(v1)d_fit_results.txt'%{"v1":i}
                #file_tmplt = 'LLM_Spctrm_I_%(v1)d_fit_results.txt'%{"v1":i}
                #file_tmplt = filetmplt%{"v1":Vvals[i]}
                file_tmplt = filetmplt%{"v1":Vvolts[i]}
                if glob.glob(file_tmplt):
                    hv_data = []; marks = []; labels = []
                    data = numpy.loadtxt(file_tmplt, delimiter = ',')
                    if CONVERT_TO_dBm:
                        data[1] = Common.list_convert_mW_dBm(data[1] / scale_factor)
                        data[2] = Common.list_convert_mW_dBm(data[2] / scale_factor)
                        data[4] = Common.list_convert_mW_dBm(data[4] / scale_factor)
                    hv_data.append([data[0], data[1]]); labels.append('Raw PSD'); marks.append(Plotting.labs_lins[0])
                    hv_data.append([data[0], data[2]]); labels.append('Voigt'); marks.append(Plotting.labs_lins[1])
                    hv_data.append([data[0], data[4]]); labels.append('Lorentz'); marks.append(Plotting.labs_lins[2])

                    # make the plot
                    args = Plotting.plot_arg_multiple()

                    args.loud = False
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'Frequency / kHz'
                    args.y_label = 'Spectral Power / dBm / 500Hz' if CONVERT_TO_dBm else 'Spectral Power / pW / 500Hz'
                    args.fig_name = file_tmplt.replace('.txt','')
                    args.plt_range = [-125, 125, -120, -20] if CONVERT_TO_dBm else [-125, 125, 0, 10]
                    args.plt_title = 'f$_{b}$ = %(v1)d MHz, D$_{eff}$ = %(v2)d km'%{"v1":Vvolts[i], "v2":(i+1)*50}

                    Plotting.plot_multiple_curves(hv_data, args)

                    hv_data.clear(); labels.clear(); marks.clear();

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Voigt_Fit_Analysis():

    # examine the fitted Voigt and Lorentz fit parameters
    # File contains data in columns of the form
    # col -1:Filename,col 0:Actual Peak / uW,col 1:Voigt h / uW,col 2:Voigt f_{0} / MHz,col 3:Voigt gamma / MHz,col 4:Voigt sigma / MHz,
    # col 5:Voigt delta / MHz,col 6:Voigt peak / uW,col 7:Lorentz h / uW,col 8:Lorentz f_{0} / MHz,col 9:Lorentz gamma / MHz,col 10:Lorentz peak / uW
    # indices of cols in file decremented by one to show there place in storage array data
    # R. Sheehan 13 - 12 - 2021

    FUNC_NAME = ".Voigt_Fit_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Sample_Data/'
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/NKT_LCR_DSHI/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            #Vvals = ['000','100','200','300','325','350','360','365','370','375','400']
            #Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]
            #Vvolts = numpy.arange(80, 2965, 80)

            #vals = numpy.arange(17)
            #vals = numpy.arange(11)
            #vals = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]
            vals = numpy.arange(80, 2965, 80)
            
            VALUES = False

            file_tmplt = 'Fitted_Parameter_Values.txt' if VALUES else 'Fitted_Parameter_GOF.txt'
            if glob.glob(file_tmplt):
                hv_data = []; marks = []; labels = []
                if VALUES:
                    data = numpy.loadtxt(file_tmplt, delimiter = ',', skiprows = 1, unpack = True, usecols = list(range(1, 12)))
                else:
                    data = numpy.loadtxt(file_tmplt, delimiter = ',', skiprows = 1, unpack = True, usecols = list(range(1, 10)))

                # Peak Vals
                PEAK_VALS = False
                if PEAK_VALS and VALUES:
                    data[0] = Common.list_convert_mW_dBm(data[0]/1e+6)
                    data[6] = Common.list_convert_mW_dBm(data[6]/1e+6)
                    data[10] = Common.list_convert_mW_dBm(data[10]/1e+6)
                    hv_data.append([vals, data[0]]); labels.append('Raw PSD Peak'); marks.append(Plotting.labs_pts[0])
                    hv_data.append([vals, data[6]]); labels.append('Voigt Peak'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[10]]); labels.append('Lorentz Peak'); marks.append(Plotting.labs_pts[2])
                    f_ending = '_peaks'
                    y_lab = 'PSD Peak Values / dBm / 500Hz'
                    x_lab = 'Beat Frequency / MHz'

                ## HWHM Vals
                HWHM_VALS = False
                if HWHM_VALS and VALUES:
                    hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[9]]); labels.append('Lorentz HWHM'); marks.append(Plotting.labs_pts[2])
                    f_ending = '_HWHM'
                    y_lab = 'Fitted HWHM / kHz'
                    x_lab = 'Beat Frequency / MHz'

                ## Voigt Fit Parameters Vals
                VOIGT_FIT_VALS = False
                if VOIGT_FIT_VALS and VALUES:
                    hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[3]]); labels.append(r'Voigt $\gamma$'); marks.append(Plotting.labs_pts[2])
                    hv_data.append([vals, data[4]]); labels.append(r'Voigt $\sigma$'); marks.append(Plotting.labs_pts[3])
                    f_ending = '_Voigt_vals'
                    y_lab = 'Voigt Fit Parameters / kHz'
                    x_lab = 'Beat Frequency / MHz'

                ## GOF chisq values
                CHISQ = False
                if CHISQ and not VALUES:
                    hv_data.append([vals, data[0]]); labels.append('Voigt'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[4]]); labels.append('Lorentz'); marks.append(Plotting.labs_pts[2])
                    f_ending = '_Fit_Chisq'
                    y_lab = r'Model Fit $\chi^{2}$'
                    x_lab = 'Beat Frequency / MHz'

                 ## GOF chisq values
                RED_CHISQ = True
                if RED_CHISQ and not VALUES:
                    hv_data.append([vals, data[2]]); labels.append('Voigt'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[6]]); labels.append('Lorentz'); marks.append(Plotting.labs_pts[2])
                    f_ending = '_Fit_Red_Chisq'
                    y_lab = r'Model Fit Reduced $\chi^{2}$'
                    x_lab = 'Beat Frequency / MHz'

                ## HWHM Vals
                #sub_data = []
                #for i in range(0, len(data[5]), 1):
                #    sub_data.append([data[5, i], data[3, i], data[4, i]])
                #Common.sort_multi_col(sub_data)

                ##hv_data.append([data[5], data[3]]); labels.append(r'Lorentz $\gamma$'); marks.append(Plotting.labs_pts[1])
                ##hv_data.append([data[5], data[4]]); labels.append(r'Gauss $\sigma$'); marks.append(Plotting.labs_pts[2])
                #hv_data.append([Common.get_col(sub_data,0), Common.get_col(sub_data,1)]); labels.append(r'Lorentz $\gamma$'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([Common.get_col(sub_data,0), Common.get_col(sub_data,2)]); labels.append(r'Gauss $\sigma$'); marks.append(Plotting.labs_pts[2])
                #f_ending = '_Voigt_cpts'

                ## Model Vals
                ## Compare the computed values of Voigt HWHM with the model 
                ## check out the following for performing 2D nonlinear fits
                ## https://lmfit.github.io/lmfit-py/examples/example_two_dimensional_peak.html
                ## https://scipython.com/blog/non-linear-least-squares-fitting-of-a-two-dimensional-data/
                ## not sure it's worth the effort to be honest
                ## need to have an interpolating function that can return Voigt delta given 
                #model_delta = []
                #model_diff = []
                #c1=0.5*1.0692; c2=0.25*0.866639; c3=0.25*4.0; c4 = math.sqrt(2.0*math.log(2.0)); 
                #for i in range(0, len(data[5]), 1):
                #    model_val = (c1*data[3][i] + math.sqrt(c2*(data[3][i]**2)+c3*(data[4][i])**2) )
                #    model_delta.append( model_val )

                #    model_diff.append(model_val - data[5][i])
                #hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([vals, model_delta]); labels.append('Model HWHM'); marks.append(Plotting.labs_pts[2])
                ##hv_data.append([vals, model_diff]); labels.append('Model - Voigt'); marks.append(Plotting.labs_pts[3])
                #f_ending = '_HWHM_Model'

                ## make the plot
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = x_lab
                args.y_label = y_lab
                args.fig_name = file_tmplt.replace('.txt',f_ending)
                args.log_y = CHISQ

                Plotting.plot_multiple_curves(hv_data, args)

                hv_data.clear(); labels.clear(); marks.clear();

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def NKT_PSD_Plot():

    # make a plot of the measured LLM DSHI spectrum for the NKT laser
    # stated NKT LL is sub-kHz, so not expecting to be able to measure NKT LL using DSHI
    # this is in fact what occurs
    # R. Sheehan 7 - 1 - 2022

    FUNC_NAME = ".NKT_PSD_Plot()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_DIR = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/DSHI_NKT/'

        if os.path.isdir(DATA_DIR):
            os.chdir(DATA_DIR)
            print(os.getcwd())

            Dlist = [25, 50, 75]
            file_tmplt = 'NKT_D_%(v1)d_Pin_8.txt'

            hv_data = []; marks = []; labels = [];
            for i in range(0, len(Dlist), 1):
                filename = file_tmplt%{"v1":Dlist[i]}
                if glob.glob(filename):
                    data = numpy.loadtxt(filename, unpack = True)
                    hv_data.append(data); 
                    marks.append(Plotting.labs_lins[i])
                    labels.append('D = %(v1)d km'%{"v1":Dlist[i]})

            # make the plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency / MHz'
            args.y_label = 'Spectral Power / dBm'
            args.fig_name = 'NKT_LLM_DSHI'
            args.plt_range = [78, 82, -80, 0]

            Plotting.plot_multiple_curves(hv_data, args)

            hv_data.clear(); labels.clear(); marks.clear();

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def NKT_Spectral_Tune():
    
    # Plot the measured spectra of the NKT laser
    # where the laser wavelength has been changed
    # R. Sheehan 9 - 2 - 2022

    FUNC_NAME = ".NKT_Spectral_Tune()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_DIR = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/NKT_Spectra/'

        os.chdir(DATA_DIR)

        args = Plotting.plot_arg_single()

        args.loud = True
        args.x_label = r'$I_{set}$ mA'
        args.y_label = r'$\lambda_{meas}$ nm'
        args.plt_range = [100, 200, 1549.7, 1550.4]
        args.plt_title = r'$T_{set}$ = 25 C, $\lambda_{set}$ = 1550 nm'
        args.fig_name = 'NKT_Current_Tuning_meas_WL'
       
        Ivals = numpy.arange(100,210,20)
        lam_vals = [1550.054, 1550.053, 1550.053, 1550.052, 1550.052, 1550.051]
        Plotting.plot_single_linear_fit_curve(Ivals, lam_vals, args)
        
        Ivals_files = ["W0000.txt", "W0001.txt", "W0002.txt", "W0003.txt", "W0004.txt", "W0005.txt"]
        Ivals_labels = [r'$I_{set}$ = 100 mA', r'$I_{set}$ = 120 mA', r'$I_{set}$ = 140 mA', r'$I_{set}$ = 160 mA', r'$I_{set}$ = 180 mA', r'$I_{set}$ = 200 mA']

        SpctrmPlt.multiple_optical_spectrum_plot(DATA_DIR, Ivals_files, Ivals_labels, [1549, 1551, -50, 10], r'$T_{set}$ = 25 C, $\lambda_{set}$ = 1550 nm', 'NKT_Current_Tuning')

        lam_vals = [1549.7, 1549.8, 1549.9, 1550.0, 1550.1, 1550.2, 1550.3]
        lam_vals_meas = [1549.750, 1549.849, 1549.948, 1550.048, 1550.147, 1550.247, 1550.348]

        args.loud = True
        args.x_label = r'$\lambda_{set}$ nm'
        args.y_label = r'$\lambda_{meas}$ nm'
        args.plt_range = [1549.7, 1550.4, 1549.7, 1550.4]
        args.plt_title = r'$T_{set}$ = 25 C, $I_{set}$ = 150 mA'
        args.fig_name = 'NKT_Wavelength_Tuning_meas_WL'

        Plotting.plot_single_linear_fit_curve(lam_vals, lam_vals_meas, args)

        Ivals_files = ["W0006.txt", "W0007.txt", "W0008.txt", "W0009.txt", "W0010.txt", "W0011.txt", "W0012.txt"]
        Ivals_labels = [r'$\lambda_{set}$ = 1549.7 nm', r'$\lambda_{set}$ = 1549.8 nm', r'$\lambda_{set}$ = 1549.9 nm', r'$\lambda_{set}$ = 1550.0 nm', r'$\lambda_{set}$ = 1550.1 nm', r'$\lambda_{set}$ = 1550.2 nm', r'$\lambda_{set}$ = 1550.3 nm']

        SpctrmPlt.multiple_optical_spectrum_plot(DATA_DIR, Ivals_files, Ivals_labels, [1549, 1551, -50, 10], r'$T_{set}$ = 25 C, $I_{set}$ = 150 mA', 'NKT_Wavelength_Tuning')

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def sort_LCR_DSHI_filenames(filename_list, loud = False):
    # sort the filenames containing the LCR-DSHI data
    # LCR-DSHI filename of the form: Beat_Data_Nmeas_%(v1)d_I_%(v2)d_%(dd)d_%(mm)d_%(yyyy)d_%(hr)d_%(min)d.txt
    # want to return a sorted list of filenames sort according date, time because you want to group together all sequential measurements    
    # Also want to break the filenames up into distinct groups
    # R. Sheehan 25 - 2 - 2022

    FUNC_NAME = ".sort_LCR_DSHI_filenames()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if filename_list is not None else False
        c2 = True if len(filename_list) > 0 else False
        c10 = c1 and c2

        if c10:
            # Python is just the fucking best sometimes
            # sort a list of filenames according to the time at which they were modified
            # see here for details
            # https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
            filename_list.sort(key=os.path.getmtime)

            # count the numbers of groups of measurements
            # find the position in the list where the group starts
            ngrp = 0
            grp_indx_lst = []
            for i in range(0,len(filename_list), 1):
                vals = Common.extract_values_from_string(filename_list[i])
                if int(vals[0]) == 0:
                    ngrp = ngrp + 1 # count the groups
                    grp_indx_lst.append(i)# store the location of the start of each group
            if loud:
                print('No. meas. groups: ',ngrp," , Group start list: ",grp_indx_lst)
                print('')

            # separate the measurement groups into distinct sets
            j=0
            the_groups = []
            while j < ngrp:
                i=0
                sub_group = []
                while i < len(filename_list):
                    if j < ngrp - 1 and i >= grp_indx_lst[j] and i < grp_indx_lst[j+1]:
                        sub_group.append(filename_list[i])
                    elif j == ngrp-1 and i >= grp_indx_lst[j]:
                        sub_group.append(filename_list[i])
                    i = i + 1
                the_groups.append(sub_group)
                if loud:
                    print(the_groups[j])
                    print('')         
                j = j + 1

            return the_groups
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nInput filename_list is empty'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LCR_DSHI_Initial_Plots():

    # plot the data measured during LCR-DSHI beat note measurement
    # ultimately you want a plot of measured linewidth versus beat note
    # scan measures linewidth for each beat note - a data frame is generated for each scan
    # multiple scans are performed - the idea then is to determine the average of all the data from each data frame
    # R. Sheehan 25 - 2 - 2021

    FUNC_NAME = ".LCR_DSHI_Initial_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_JDSU_DFB_T_20_D_10/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # obtain ordered list of file names
            filelst = glob.glob('Beat*.txt')
            
            meas_grp_lst = sort_LCR_DSHI_filenames(filelst, False)

            # measurement sets to be analysed
            for i in range(0, len(meas_grp_lst), 1):
                for j in range(0, len(meas_grp_lst[i]), 1):
                    print(meas_grp_lst[i][j])
                print('')

            # read in the data file using pandas
            i = j = 1
            data = pandas.read_csv(meas_grp_lst[i][j], delimiter = '\t', skiprows = [0, 2])

            titles = list(data)

            print(titles, ", len(titles) = ", len(titles), ", len(data) = ", data.shape[1])
            print('')
            #pprint.pprint(data)
            n = 10
            
            #print(data[titles[n]])

            # make a basic plot
            args = Plotting.plot_arg_single()

            n = 0
            m = 10

            print(titles[n])
            print(titles[m])

            args.loud = True
            #args.crv_lab_list = labels
            #args.mrk_list = marks
            args.x_label = titles[n]
            args.y_label = titles[m]
            #args.fig_name = 'NKT_LLM_DSHI'
            #args.plt_range = [78, 82, -80, 0]

            Plotting.plot_single_curve(data[titles[n]], data[titles[m]], args)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate dir: ' + DATA_HOME
            raise EnvironmentError
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Parse_OEWaves_file(filename, loud = False):

    # read the output file from the OEwaves system
    # parse the contents for useful data
    # looking for: 
    # measurement type, measurement settings, comments, OEwaves settings, measurement data
    # R. Sheehan 1 - 3 - 2022

    # Frequency units Hz
    # RIN units dBc / Hz
    # Phase Noise units dBc / Hz
    # Spurious units dBc
    # Frequency Noise units Hz^{2} / Hz
    # Frequency Noise units Hz / Hz^{1/2}

    FUNC_NAME = ".Parse_OEWaves_file()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if(glob.glob(filename)):
            n_preamble_rows = 12

            # read the pre-amble data
            preamble = Common.head(filename, n_preamble_rows)
                        
            meas_type = preamble[0].replace(' Measurement Data\n','') # extract meas. type from preamble
            print('Measurement Type: ',meas_type)

            LL_data = []

            if 'Phase' in meas_type:
                vals = Common.extract_values_from_string(preamble[-1]) # extract measured LL from preample
                n_elw = 4 # ideally there would be 4 Ext. LW measurements
                n_occur = preamble[-1].count('N/A') # ideally n_occur = 0, however, sometimes it's 1, 2, 3?                
                instantaneous_ll = float(vals[5])/1000.0 # instantaneous LL in units of kHz
                if loud: 
                    print(vals)
                    print("Length(vals) = ", len(vals))
                    print("No. occurrences of N/A: ",n_occur)

                # Extract the data for the Extended LW measurement, whatever that is
                #extended_ll_times = []
                #extended_ll_vals = []                 
                #ideal_x_indx = [13, 11, 9, 7] # ideally the data would be located at these indexes
                #ideal_y_indx = [12, 10, 8, 6]
                #for i in range(n_occur, n_elw, 1):
                #    extended_ll_times.append( float( vals[ ideal_x_indx[ i ] ] ) )
                #    extended_ll_vals.append( float( vals[ ideal_y_indx[ i ] ] ) )

                # Extract the data for the Extended LW measurement
                # this time put a zero wherever there is an N/A value
                # this simplifies the data munging down the line
                extended_ll_times = [0.1, 1, 10, 100]
                extended_ll_vals = [0.0, 0.0, 0.0, 0.0]                 
                ideal_x_indx = [13, 11, 9, 7] # ideally the data would be located at these indexes
                ideal_y_indx = [12, 10, 8, 6] # ideally the data would be located at these indexes
                for i in range(n_occur, n_elw, 1):
                    extended_ll_vals[i] = float( vals[ ideal_y_indx[ i ] ] )
                
                #if 'N/A' in preamble[-1]:
                #    extended_ll_times = [float(vals[-2]), float(vals[-4]), float(vals[-6])] # extended LL observation times in units of ms
                #    extended_ll_vals = [float(vals[-3]), float(vals[-5]), float(vals[-7])]
                #else:
                #    extended_ll_times = [float(vals[-1]), float(vals[-3]), float(vals[-5]), float(vals[-7])] # extended LL observation times in units of ms
                #    extended_ll_vals = [float(vals[-2]), float(vals[-4]), float(vals[-6]), float(vals[-8])]

                LL_data.append(extended_ll_times)
                LL_data.append(extended_ll_vals)
                
                if loud:
                    print('Extended LL Obs. Times: ',extended_ll_times,' ms')
                    print('Extended LL: ',extended_ll_vals,' kHz')
                    print('Avg. Extended LL: ',numpy.mean(extended_ll_vals),' kHz')
                    print('Instantaneous LL: ',instantaneous_ll,' kHz')
                    print('')

            #read the measured data
            measured_data = numpy.loadtxt(filename, delimiter = '\t', skiprows = n_preamble_rows, unpack = True)

            if loud: print("Data dimensions (cols, rows) = ", measured_data.shape)

            return [meas_type, measured_data, LL_data, instantaneous_ll]
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + filename
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OEWaves_Analysis_Single(filename, loud = False):

    # Analyse data measured by the OEWaves OE4000
    # plot the FNPSD, RIN and Extended LL measurement data for a single measurement
    # R. Sheehan 3 - 3 - 2022

    FUNC_NAME = ".OEWaves_Analysis_Single()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if(glob.glob(filename)):
            
            ret_val = Parse_OEWaves_file(filename, loud)

            if len(ret_val) > 0:
                if 'Phase' in ret_val[0]: 
                    # Make a plot of the measured instantaneous extended measured linewidth data
                    args = Plotting.plot_arg_single()
                    
                    args.loud = loud
                    args.marker = Plotting.labs_pts[3]
                    args.x_label = 'Observation Time ( ms )'
                    args.y_label = 'Linewidth ( kHz )'
                    args.fig_name = filename.replace('.txt','_LL')
                    args.log_x = True
                    args.log_y = False            

                    Plotting.plot_single_curve(ret_val[2][0], ret_val[2][1], args)

                    # make a plot of the Phase Noise in units of Hz^{2} / Hz
                    # include the beta-line in the plot

                    #plt_indx = 1 # this is the indx of the column storing the Phase Noise data in units of dBc / Hz
                    #plt_indx = 2 # this is the indx of the column storing the Spurious Noise data in units of dBc / Hz
                    #plt_indx = 4 # this is the indx of the column storing the FNPSD data in units of Hz / Hz^{1/2}
                    plt_indx = 3 # this is the indx of the column storing the FNPSD data in units of Hz^{2} / Hz

                    hv_data = []; marks = []; labels = []

                    # measured frequency noise
                    hv_data.append([ret_val[1][0], ret_val[1][plt_indx]]); 
                    marks.append(Plotting.labs_lins[0]); 
                    labels.append('S(f)')
                    
                    # beta-line
                    beta_slope = (8.0*math.log(2.0)) / (math.pi**2)
                    hv_data.append([[ret_val[1][0][0], ret_val[1][0][-1]],[beta_slope*ret_val[1][0][0], beta_slope*ret_val[1][0][-1]]]); 
                    marks.append(Plotting.labs_dashed[6]); 
                    labels.append('c f')

                    # make the plot including the beta-line
                    args = Plotting.plot_arg_multiple()

                    args.loud = loud
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'Frequency ( Hz )'
                    args.y_label = 'Frequency Noise ( Hz$^{2}$ / Hz )'
                    args.fig_name = filename.replace('.txt','')
                    args.log_x = True
                    args.log_y = True                   

                    Plotting.plot_multiple_curves(hv_data, args)
                else:
                    # make a plot of the RIN in units of dBc / Hz
                    args = Plotting.plot_arg_single()
                    plt_indx = 1
                    args.loud = loud
                    #args.curve_label = 'JDSU DFB Laser'
                    #args.curve_label = 'NKT Fibre Laser'
                    args.marker = Plotting.labs_lins[0]
                    args.x_label = 'Frequency ( Hz )'
                    args.y_label = 'RIN / dBc ( Hz )'
                    args.fig_name = filename.replace('.txt','')
                    args.log_x = True
                    args.log_y = False            

                    Plotting.plot_single_curve(ret_val[1][0], ret_val[1][plt_indx], args)
            
                del ret_val
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + filename
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OEWaves_RIN_Multiple(filelst, laser_name, loud = False):
    # Analyse data measured by the OEWaves OE4000
    # plot the RIN data for multiple measurements
    # R. Sheehan 3 - 3 - 2022

    FUNC_NAME = ".OEWaves_RIN_Multiple()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        hv_data = []; marks = []; labels = []; 
        count = 0
        for f in filelst:
            ret_val = Parse_OEWaves_file(f)
            if 'RIN' in ret_val[0]:
                hv_data.append(ret_val[1]); 
                marks.append( Plotting.labs_lins[ count%len(Plotting.labs_lins) ] ); 
                labels.append('M %(v1)d'%{"v1":count+1})
                count = count + 1

        # Plot the data sets on a single graph
        args = Plotting.plot_arg_multiple()

        args.loud = loud
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Frequency ( Hz )'
        args.y_label = 'RIN / dBc ( Hz )'
        args.fig_name = laser_name + '_RIN'
        args.log_x = True
        args.log_y = False                  

        Plotting.plot_multiple_curves(hv_data, args)

        del hv_data; del marks; del labels; del ret_val; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OEWaves_FNPSD_Multiple(filelst, laser_name, loud = False):
    # Analyse data measured by the OEWaves OE4000
    # plot the FNPSD data for multiple measurements
    # R. Sheehan 3 - 3 - 2022

    FUNC_NAME = ".OEWaves_FNPSD_Multiple()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        ll_data = []; instant_ll = []; hv_data = []; ll_marks = []; marks = []; labels = []; 
        plt_indx = 3 # this is the indx of the column storing the FNPSD data
        count = 0
        for f in filelst:
            ret_val = Parse_OEWaves_file(f)
            if 'Phase' in ret_val[0]:
                hv_data.append([ret_val[1][0], ret_val[1][plt_indx]]); 
                ll_data.append(ret_val[2])
                instant_ll.append(ret_val[3])
                ll_marks.append( Plotting.labs_pts[ count%len(Plotting.labs_pts) ] ); 
                marks.append( Plotting.labs_lins[ count%len(Plotting.labs_lins) ] ); 
                labels.append('M %(v1)d'%{"v1":count+1})
                count = count + 1

        avg_ll = numpy.mean(instant_ll)
        delta_ll = 0.5*(numpy.max(instant_ll) - numpy.min(instant_ll))

        if loud:
            print("Average Instantaneous LL")
            print("LL_int_avg = %(v1)0.3f +/- %(v2)0.3f kHz"%{"v1":avg_ll, "v2":delta_ll})
            print("LL_int_avg = %(v1)0.3f +/- %(v2)0.3f MHz"%{"v1":avg_ll/1000.0, "v2":delta_ll/1000.0})
            print("")

        # Make a histogram of the instantaneous LW measurements
        args = Plotting.plot_arg_single()

        args.loud = loud
        args.x_label = 'Instantaneous LW ( kHz )'
        args.y_label = 'Frequency'
        args.fig_name = laser_name + '_instantaneous_LW'
        args.plt_title = "LL_int_avg = %(v1)0.3f +/- %(v2)0.3f kHz"%{"v1":avg_ll, "v2":delta_ll}

        Plotting.plot_histogram(instant_ll, args)        

        # determine the average of all the extended LL values
        arr_tmp = []
        for i in range(0, len(ll_data), 1):
            arr_tmp.append(ll_data[i][1])

        arr_tmp = Common.transpose_multi_col(arr_tmp)

        avg_LL = []; err_LL = []; 
        for i in range(0, len(arr_tmp), 1):
            avg_LL.append(numpy.mean(arr_tmp[i]))
            err_LL.append( 0.5*(numpy.max(arr_tmp[i]) - numpy.min(arr_tmp[i])) )

        ll_data.append([ll_data[0][0], avg_LL]); ll_marks.append('kx--'); labels.append('Avg')

        del arr_tmp; 

        # Plt the extended LL with error bars
        args = Plotting.plot_arg_single()

        args.loud = loud
        args.x_label = 'Observation Time ( ms )'
        args.y_label = 'Linewidth ( kHz )'
        args.fig_name = laser_name + '_FNPSD_extended_LL_err'
        args.log_x = True
        args.log_y = False 
        args.show_leg = False
        #args.plt_range = [0.08, 120, 1000, 6000]
        #args.plt_range = [0.08, 120, 10, 300]
        #args.plt_range = [0.08, 120, 0.0, 40]

        Plotting.plot_single_curve_with_errors(ll_data[0][0], avg_LL, err_LL, args)

        # write the various estimates of the LL to a single file
        # write the averaged extended LL data to a file
        # Redirect the output to a file
        LL_res_file = laser_name + '_LL_Results.txt'
        old_target, sys.stdout = sys.stdout, open(LL_res_file, 'w')

        ext_avg_ll = numpy.mean( avg_LL ) if math.fabs(avg_LL[0]) > 0.0 else numpy.mean( avg_LL[1:-1] )
        ext_delta_ll = numpy.mean( err_LL ) if math.fabs(err_LL[0]) > 0.0 else numpy.mean( err_LL[1:-1] )
        
        print('Observation Time (ms),\tExtended LL (kHz)')
        for i in range(0, len(avg_LL), 1):
            print('%(v1)0.3f,\t%(v2)0.3f,\t%(v3)0.3f'%{"v1":ll_data[0][0][i], "v2":avg_LL[i], "v3":err_LL[i]})
        print("")
        print("Average Extended LL")
        print("LL_ext_avg = %(v1)0.3f +/- %(v2)0.3f kHz"%{"v1":ext_avg_ll, "v2":ext_delta_ll})
        print("LL_ext_avg = %(v1)0.3f +/- %(v2)0.3f MHz"%{"v1":ext_avg_ll/1000.0, "v2":ext_delta_ll/1000.0})
        print("")

        int_avg_ll = numpy.mean(instant_ll)
        delta_ll = 0.5*(numpy.max(instant_ll) - numpy.min(instant_ll))
        print("Average Instantaneous LL")
        print("LL_int_avg = %(v1)0.3f +/- %(v2)0.3f kHz"%{"v1":int_avg_ll, "v2":delta_ll})
        print("LL_int_avg = %(v1)0.3f +/- %(v2)0.3f MHz"%{"v1":int_avg_ll/1000.0, "v2":delta_ll/1000.0})
        print("")
        
        sys.stdout = old_target # return to the usual stdout

        # Plot the data sets on a single graph
        args = Plotting.plot_arg_multiple()
                
        # Extended LL Plot
        args.loud = loud
        args.crv_lab_list = labels
        args.mrk_list = ll_marks
        args.x_label = 'Observation Time ( ms )'
        args.y_label = 'Linewidth ( kHz )'
        args.fig_name = laser_name + '_FNPSD_extended_LL'
        args.log_x = True
        args.log_y = False  
        args.show_leg = False
        #args.plt_range = [0.08, 120, 1000, 6000]
        #args.plt_range = [0.08, 120, 10, 300]
        #args.plt_range = [0.08, 120, 0.0, 40]

        Plotting.plot_multiple_curves(ll_data, args) 
                
        # FNPSD Plot    
        # beta-line
        beta_slope = (8.0*math.log(2.0)) / (math.pi**2)
        hv_data.append( [ [ret_val[1][0][0], ret_val[1][0][-1]], [beta_slope*ret_val[1][0][0], beta_slope*ret_val[1][0][-1]] ] ); 
        marks.append(Plotting.labs_dashed[6]); 
        labels.pop(); labels.append('c f')       

        args.loud = loud
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Frequency ( Hz )'
        args.y_label = 'Frequency Noise ( Hz$^{2}$ / Hz )'
        args.fig_name = laser_name + '_FNPSD'
        args.log_x = True
        args.log_y = True  
        args.show_leg = False
        #args.plt_range = [10, 1e+6, 1e+1, 1e+12]

        Plotting.plot_multiple_curves(hv_data, args)

        del ll_data; del hv_data; del marks; del labels; del ret_val; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OEWaves_FNPSD_Integration(filelst, laser_name, loud = False):
    # Analyse data measured by the OEWaves OE4000
    # estimate LL from the FNPSD data from multiple measurements
    # asume that LL can be approximated according to the technique presented in
    # Domenico et al, ``Simple approach to the relation between laser frequency 
    # noise and laser line shape'', Appl. Opt., 49 (25), 2010
    # R. Sheehan 3 - 3 - 2022

    FUNC_NAME = ".OEWaves_FNPSD_Integration()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        hv_data = []; 
        plt_indx = 3 # this is the indx of the column storing the FNPSD data
        for f in filelst:
            ret_val = Parse_OEWaves_file(f)
            if 'Phase' in ret_val[0]:
                hv_data.append([ret_val[1][0], ret_val[1][plt_indx]]);  

        del ret_val;
        
        # Approximate the integral of the FNPSD in the region where S > beta-slope * f
        # see Domenico et al, Appl. Opt., 49 (25), 2010 for details
        if len(hv_data)>0:
            # proceed with integration
            
            # beta-line
            beta_slope = (8.0*math.log(2.0)) / (math.pi**2)
            #print('beta data = [ [',hv_data[0][0][0],', ',hv_data[0][0][-1],' ], [',hv_data[0][0][0]*beta_slope,', ',hv_data[0][0][-1]*beta_slope,' ] ]')
            #print('')

            appr_lst = []
            for i in range(0, len(hv_data), 1):
                integral = 0
                for j in range(1, len(hv_data[i][0]), 1):
                    # only compute the integral in the regions where S > beta-slope * f
                    # and for frequencies where noise is dominated by 1/f noise, i.e. f < 100 kHz
                    # argument goes that for f > 100 kHz noise is purely Gaussian and therefore does
                    # not contribute significantly to LL
                    if hv_data[i][0][j] < 1e+5 and hv_data[i][1][j] > beta_slope * hv_data[i][0][j]:
                        integral = integral + ( hv_data[i][0][j] - hv_data[i][0][j-1] ) * hv_data[i][1][j]
                print('Integral ',i,': ',integral,', HWHM: ',0.5*math.sqrt(8.0*integral))
                appr_lst.append( 0.5*math.sqrt(8.0*integral) ) # Are you sure this is correct? Is there a multiplicative factor of log(2) missing? RNS 12 - 2 - 2025

            #appr_lst = []
            #for i in range(0, len(hv_data), 1):
            #    integral = 0
            #    for j in range(1, len(hv_data[i][0]), 1):
            #        term = ( hv_data[i][0][j] - hv_data[i][0][j-1] ) * hv_data[i][1][j] if hv_data[i][1][j] > beta_slope * hv_data[i][0][j] else 0.0
            #        integral = integral + term
            #    print('Integral ',i,': ',integral,', HWHM: ',0.5*math.sqrt(8.0*integral))
            #    appr_lst.append( 0.5*math.sqrt(8.0*integral) )

            avg_integral = numpy.mean(appr_lst); 
            delta_integral = 0.5*( numpy.max(appr_lst) - numpy.min(appr_lst) )
            rel_error = delta_integral / avg_integral
            print('HWHM: ',avg_integral,' +/-',delta_integral,' Hz')
            print('HWHM: ',avg_integral/1e+3,' +/-',delta_integral/1e+3,' kHz')
            print('HWHM: ',avg_integral/1e+6,' +/-',delta_integral/1e+6,' MHz')
            print('Rel. Error: ',rel_error)
            print('')

            # write the various estimates of the LL to a single file
            # Redirect the output to a file
            LL_res_file = laser_name + '_LL_Results.txt'
            old_target, sys.stdout = sys.stdout, open(LL_res_file, 'a')

            print("Sum Over PSD LL")
            print("LL_sum_avg = %(v1)0.3f +/- %(v2)0.3f kHz"%{"v1":avg_integral/1e+3, "v2":delta_integral/1e+3})
            print("LL_sum_avg = %(v1)0.3f +/- %(v2)0.3f MHz"%{"v1":avg_integral/1e+6, "v2":delta_integral/1e+6})
            print("")
        
            sys.stdout = old_target # return to the usual stdout

            # Make a histogram of the summed LW measurements
            args = Plotting.plot_arg_single()

            args.loud = loud
            args.x_label = 'Summed LW ( kHz )'
            args.y_label = 'Frequency'
            args.fig_name = laser_name + '_summed_LW'
            args.plt_title = "LL_sum_avg = %(v1)0.3f +/- %(v2)0.3f kHz"%{"v1":avg_integral/1e+3, "v2":delta_integral/1e+3}

            for i in range(0, len(appr_lst), 1): appr_lst[i] = appr_lst[i] / 1e+3

            Plotting.plot_histogram(appr_lst, args)

            del hv_data;  
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nIntegration not possible\nNo data available'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OEWaves_Analysis():

    # Analyse data measured by the OEWaves OE4000
    # R. Sheehan 1 - 3 - 2022

    FUNC_NAME = ".OEWaves_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/OE4000_Init/NKT_High_Averaging_With_Isolator/'
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/OE4000_Init/CoBrite_TLS_High_Averaging_With_Isolator/'

        if(os.path.isdir(DATA_HOME)):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #filename = 'JDSU_DFB_T_20_I_50_PN_1.txt'
            #filename = 'JDSU_DFB_T_20_I_50_RIN_2.txt'
            #filename = 'NKT_T_25_I_110_FN_1.txt'
            #filename = 'NKT_T_25_I_110_RIN_2.txt'
            #filename = 'NKT_I_125_1000_20_11_2023.txt'
            #filename = 'NKT_I_150_1428_20_11_2023.txt'
            #OEWaves_Analysis_Single(filename, True)

            #dev_name = 'Ref_DFB'
            dev_name = 'CoBrite'
            #dev_name = 'NKT'
            Ival = 200
            filestr = '%(v1)s_I_%(v2)d*.txt'%{"v1":dev_name, "v2":Ival}
            
            #dev_name = 'Reference_DFB'
            dev_name = 'CoBrite_Tunable'
            #dev_name = 'NKT_FL'
            resstr = '%(v1)s_P_%(v2)d'%{"v1":dev_name, "v2":Ival}

            filenames = glob.glob(filestr)
            #for f in filenames: OEWaves_Analysis_Single(f, True)
            OEWaves_FNPSD_Multiple(filenames, resstr, False)
            OEWaves_FNPSD_Integration(filenames, resstr, True)

            # JDSU DFB RIN
            filelst = ['JDSU_DFB_T_20_I_50_RIN_1.txt', 'JDSU_DFB_T_20_I_50_RIN_2.txt']
            laser_name = 'JDSU_DFB'
            #OEWaves_RIN_Multiple(filelst, laser_name, True)

            # NKT RIN
            filelst = ['NKT_T_25_I_110_RIN_1.txt', 'NKT_T_25_I_110_RIN_2.txt']
            laser_name = 'NKT'
            #OEWaves_RIN_Multiple(filelst, laser_name, True)

            # RIN Comparison
            filelst = ['JDSU_DFB_T_20_I_50_RIN_1.txt', 'NKT_T_25_I_110_RIN_2.txt']
            laser_name = 'DFB_NKT'
            #OEWaves_RIN_Multiple(filelst, laser_name, True)

            # JDSU DFB FNPSD
            filelst = ['JDSU_DFB_T_20_I_50_PN_1.txt', 'JDSU_DFB_T_20_I_50_PN_2.txt', 'JDSU_DFB_T_20_I_50_PN_3.txt', 'JDSU_DFB_T_20_I_50_FN_1.txt', 'JDSU_DFB_T_20_I_50_FN_2.txt']
            laser_name = 'JDSU_DFB'
            #OEWaves_FNPSD_Multiple(filelst, laser_name, False)
            #OEWaves_FNPSD_Integration(filelst, True)

            # NKT FNPSD
            filelst = ['NKT_T_25_I_110_PN_1.txt', 'NKT_T_25_I_110_PN_2.txt', 'NKT_T_25_I_110_FN_1.txt', 'NKT_T_25_I_110_FN_2.txt', 'NKT_T_25_I_110_FN_3.txt']
            laser_name = 'NKT'
            #OEWaves_FNPSD_Multiple(filelst, laser_name, True)
            #OEWaves_FNPSD_Integration(filelst, True)

            # JDSU DFB NKT FNPSD Comparison
            filelst = ['JDSU_DFB_T_20_I_50_PN_3.txt', 'NKT_T_25_I_110_PN_1.txt']
            laser_name = 'DFB_NKT'
            #OEWaves_FNPSD_Multiple(filelst, laser_name, True)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception

        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Shengkai_LLM_22_2_2023/ZK Jia_test results_24_2_2023/'

        #if(os.path.isdir(DATA_HOME)):
        #    os.chdir(DATA_HOME)
        #    print(os.getcwd())

        #    #filelst = glob.glob('ZJ_Test_*_24_2_2023.txt')
            
        #    #filelst = ['ZJ_Test_1_24_2_2023.txt', 'ZJ_Test_2_24_2_2023.txt', 'ZJ_Test_3_24_2_2023.txt', 'ZJ_Test_4_24_2_2023.txt', 'ZJ_Test_5_24_2_2023.txt']
        #    #laser_name = 'ZJL_M1'
            
        #    filelst = ['ZJ_Test_6_24_2_2023.txt', 'ZJ_Test_7_24_2_2023.txt', 'ZJ_Test_8_24_2_2023.txt', 'ZJ_Test_9_24_2_2023.txt']
        #    laser_name = 'ZJL_M2'            
            
        #    OEWaves_FNPSD_Multiple(filelst, laser_name, True)
            
        #    OEWaves_FNPSD_Integration(filelst, True)

        #else:
        #    ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
        #    raise Exception

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Combine_Multi_Spctrm():

    # join together multiple multi-spectra plots into a single plot
    # also take a look at the first plot as a function of Attenuation
    # R. Sheehan 14 - 7 - 2022

    FUNC_NAME = ".Combine_Multi_Spctrm()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/MultiSpctrm/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # import the data
            filename = 'FullPltTest%(v1)d.txt'
            
            hv_data = []; marks = []; labels = []; 

            for i in range(1,6,1):
                the_file = filename%{"v1":i}
                if glob.glob(the_file):
                    the_data = numpy.loadtxt(the_file, unpack = True)
                    hv_data.append(the_data)
                    marks.append(Plotting.labs_lins[i])
                    labels.append('Sweep %(v1)d'%{"v1":i})

            # Plot the data sets on a single graph
            args = Plotting.plot_arg_multiple()
                
            # Extended LL Plot
            args.loud = False
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency ( MHz )'
            args.y_label = 'Spectral Power ( dBm )'
            args.fig_name = 'JDSU_LCR_DSHI'
            
            Plotting.plot_multiple_curves(hv_data, args)

            #del hv_data; del the_data; 

            # Plot the data obtained as a function of Attenuation
            voltages = ['00', '25', '30', '35', '40', '45']
            powers = [1.15, -0.8, -3.35, -7.8, -18.55, -26.5]

            filename = 'FullPltTest1_Vb_%(v1)sV.txt'
            
            hv_data = []; marks = []; labels = []; 

            for i in range(0,5,1):
                the_file = filename%{"v1":voltages[i]}
                if glob.glob(the_file):
                    the_data = numpy.loadtxt(the_file, unpack = True)
                    hv_data.append(the_data)
                    marks.append(Plotting.labs_lins[i])
                    labels.append(r'$P_{2}$ = %(v1)0.2f dBm'%{"v1":powers[i]})

            # Plot the data sets on a single graph
                
            # Extended LL Plot
            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency ( MHz )'
            args.y_label = 'Spectral Power ( dBm )'
            args.fig_name = 'JDSU_LCR_DSHI_with_Attenuation'
            
            Plotting.plot_multiple_curves(hv_data, args)

            del hv_data; del the_data; 

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def AOM_Temperature():

    FUNC_NAME = ".AOM_Temperature()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/AOM_Temp/'

        if os.path.isdir(DATA_HOME):

            os.chdir(DATA_HOME)

            print(os.getcwd())

            #filename = 'AOM_Temp_Versus_Time_10_8_2022.txt'
            filename = 'AOM_Temp_Versus_Time_17_10_2022.txt'

            if glob.glob(filename):
                # read the data from the file
                data = numpy.loadtxt(filename, unpack = True)
                data[0] = data[0] / (60.0*60.0) # convert time from seconds to hours

                # plot the data obtained
                hv_data = []; mrk_list = []; labels = []; 
                hv_data.append([data[0], data[1]]); mrk_list.append(Plotting.labs_pts[0]); labels.append('Air')
                hv_data.append([data[0], data[2]]); mrk_list.append(Plotting.labs_pts[1]); labels.append('AOM')
                hv_data.append([data[0], data[3]]); mrk_list.append(Plotting.labs_pts[2]); labels.append('AOM Driver')

                args = Plotting.plot_arg_multiple()
                
                # Extended LL Plot
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = mrk_list
                args.x_label = 'Time ( hrs )'
                args.y_label = 'Temperature ( C )'
                #args.plt_range = [0, 8, 22, 36]
                args.plt_range = [0, 8, 15, 30]
                args.fig_name = filename.replace('.txt','')
            
                Plotting.plot_multiple_curves(hv_data, args)

                del hv_data; 
                
                # Is there a correlation between AOM temperature and Air temperature

                # get correlation between measured AOM Temperature and Air Temperature
                # ideally this should be zero
                AOMAIRrcoeff = numpy.corrcoef(data[1], data[2])

                # get correlation between measured AOM Driver Temperature and Air Temperature
                # ideally this should be zero
                AOMDrvAIRrcoeff = numpy.corrcoef(data[1], data[3])

                # get correlation between measured AOM Driver Temperature and AOM Temperature
                # ideally this should be one
                AOMDrvAOMrcoeff = numpy.corrcoef(data[2], data[3])

                print("\nCorrelation Coefficients")
                print('AOM Temperature vs Air Temperature Correlation Coefficient: ', AOMAIRrcoeff[1][0])
                print('AOM Temperature vs Air Temperature Correlation Coefficient: ', AOMAIRrcoeff[0][1])
                print('AOM Driver Temperature vs Air Temperature Correlation Coefficient: ', AOMDrvAIRrcoeff[1][0])
                print('AOM Driver Temperature vs Air Temperature Correlation Coefficient: ', AOMDrvAIRrcoeff[0][1])
                print('AOM Driver Temperature vs AOM Temperature Correlation Coefficient: ', AOMDrvAOMrcoeff[1][0])
                print('AOM Driver Temperature vs AOM Temperature Correlation Coefficient: ', AOMDrvAOMrcoeff[0][1])

                # make some plots
                args = Plotting.plot_arg_single()
                
                args.loud = True
                #args.curve_label = ''
                #args.marker = Plotting.labs_pts[1]
                args.x_label = 'T$_{Air}$ ( C )'
                args.y_label = 'T$_{AOM}$ ( C )'
                args.plt_title = 'T$_{AOM}$ vs T$_{Air}$ r = %(v1)0.3f'%{"v1":AOMAIRrcoeff[1][0]}
                args.fig_name = 'T_AOM_vs_T_Air'                
                                               
                Plotting.plot_single_linear_fit_curve(data[1], data[2], args)

                args.x_label = 'T$_{Air}$ ( C )'
                args.y_label = 'T$_{AOM Drv}$ ( C )'
                args.plt_title = 'T$_{AOM Drv}$ vs T$_{Air}$ r = %(v1)0.3f'%{"v1":AOMDrvAIRrcoeff[1][0]}
                args.fig_name = 'T_AOM_Drv_vs_T_Air'                
                
                Plotting.plot_single_linear_fit_curve(data[1], data[3], args)

                args.x_label = 'T$_{AOM}$ ( C )'
                args.y_label = 'T$_{AOM Drv}$ ( C )'
                args.plt_title = 'T$_{AOM Drv}$ vs T$_{AOM}$ r = %(v1)0.3f'%{"v1":AOMDrvAOMrcoeff[1][0]}
                args.fig_name = 'T_AOM_Drv_vs_T_AOM'                
                
                Plotting.plot_single_linear_fit_curve(data[2], data[3], args)

                del data; 
            else:
                ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + filename
                raise Exception
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def ESA_Spctrm_Attn():

    # Make some plots of the ESA spectrum for different attenuation levels
    # Analyse the data obtained
    # R. Sheehan 9 - 11 - 2022

    FUNC_NAME = ".ESA_Spctrm_Attn()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'

        if os.path.isdir(DATA_HOME):

            os.chdir(DATA_HOME)

            print(os.getcwd())
            
            PLOT_SINGLE = False

            Vvals = ['000','100','200','300','325','350','360','365','370','375','400']
            Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]

            filetmplt = 'JDSU_DFB_T_20_I_50_V_%(v1)s.txt' if PLOT_SINGLE else 'JDSU_DFB_T_20_I_50_V_%(v1)s_Full.txt'

            # Import the data
            hv_data = []
            labels = []
            marks = []
            
            PLOT_SINGLY = False

            for ss in range(0, len(Vvals), 1): 
                filename = filetmplt%{"v1":Vvals[ss]}
                if glob.glob(filename):
                    data = numpy.loadtxt(filename, unpack = True)
                    hv_data.append(data)
                    the_label = 'V$_{VOA}$ = %(v1)0.2f V'%{"v1":Vvolts[ss]}
                    labels.append(the_label)
                    the_mark = Plotting.labs_lins[ss%len(Plotting.labs_lins)]
                    marks.append(the_mark)
                    if PLOT_SINGLY:
                        # plot each dataset as it comes in
                        # Plot the data
                        args = Plotting.plot_arg_single()
                
                        # Extended LL Plot
                        args.loud = False
                        args.curve_label = the_label
                        args.marker = the_mark
                        args.x_label = 'Beat Frequency ( MHz )'
                        args.y_label = 'Spectral Power ( dBm / 20kHz )' if PLOT_SINGLE else 'Spectral Power ( dBm / 500kHz )'
                        args.plt_range = [30, 130, -105, -70] if PLOT_SINGLE else [0, 3000, -90, -55]
                        args.fig_name = filename.replace('.txt','')
            
                        Plotting.plot_single_curve(data[0], data[1], args)

            BASIC_PLOT = False

            if BASIC_PLOT:
                # Plot the data
                args = Plotting.plot_arg_multiple()
                
                # Extended LL Plot
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Beat Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm / 20kHz )' if PLOT_SINGLE else 'Spectral Power ( dBm / 500kHz )'
                args.plt_range = [30, 130, -105, -70] if PLOT_SINGLE else [0, 3000, -90, -55]
                args.fig_name = 'ESA_Single' if PLOT_SINGLE else 'ESA_Full'
            
                Plotting.plot_multiple_curves(hv_data, args)

            FULL_ANALYSIS = True

            if FULL_ANALYSIS and PLOT_SINGLE is False:
                # Analyse the data from the full spectrum
                # Step through each file for each bias value
                # record the peak power value at each beat note
                # plot the beat note power versus frequency for each bias
                peak_data = []
                no_peaks = []
                CNR_min = 5
                for ii in range(0, len(hv_data), 1):
                    Noise_level = hv_data[ii][1][-1] if ii > 2 else -80.0
                    fbeats, pbeats = Extract_Peak_Data(hv_data[ii][0], hv_data[ii][1])
                    peak_data.append( [fbeats, pbeats] )
                    no_peaks.append(Estimate_No_Viable_Peaks(pbeats, CNR_min, Noise_level))

                # Plot the data
                args = Plotting.plot_arg_multiple()

                # Extended LL Peaks Plot
                args.loud = False
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm / 500kHz )'
                args.plt_range = [0, 3000, -90, -55]
                args.fig_name = 'ESA_Full_Peaks'
            
                #Plotting.plot_multiple_curves(peak_data, args)

                # Plot the data
                args = Plotting.plot_arg_single()

                # Extended LL Peaks Plot
                args.loud = True
                args.x_label = 'VOA Bias ( V )'
                args.y_label = 'No. Beat Signal'
                #args.plt_range = [0, 3000, -90, -55]
                args.fig_name = 'No_Peaks_VOA_Bias'
            
                Plotting.plot_single_curve(Vvolts, no_peaks, args)

                del peak_data; 

            SINGLE_ANALYSIS = False

            if SINGLE_ANALYSIS:
                # Analyse the data from the single spectra
                # Make an estimate of the signal / noise ratio based on the scheme given in the ESA Manual
                
                signal = []
                noise = []
                SNR = []
                sig_range = [60, 100]
                for ii in range(0, len(hv_data), 1):
                    ret_val = Estimate_SNR(hv_data[ii][0], hv_data[ii][1], sig_range)
                    signal.append(ret_val[0])
                    noise.append(ret_val[1])
                    SNR.append(ret_val[2])

                SNR_data = []
                SNR_data.append([Vvolts, signal])
                SNR_data.append([Vvolts, noise])
                SNR_data.append([Vvolts, SNR])

                # Plot the data
                args = Plotting.plot_arg_multiple()
                
                # Extended LL Plot
                args.loud = True
                args.crv_lab_list = ['Signal','Noise','SNR']
                args.mrk_list = Plotting.labs[0:3]
                args.x_label = 'VOA Bias ( V )'
                args.y_label = 'SNR'
                #args.plt_range = [30, 130, -105, -70] if PLOT_SINGLE else [0, 3000, -90, -55]
                args.fig_name = 'SNR_Estimate'
            
                Plotting.plot_multiple_curves(SNR_data, args)

                del SNR_data; del signal; del noise; del SNR; 

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Extract_Peak_Data(frq, power):
    # scan the frq, power data set and return the power values at each of the beat note frequencies

    FUNC_NAME = ".Extract_Peak_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if len(frq) > 0 else False
        c2 = True if len(power) > 0 else False
        c3 = True if len(frq) == len(power) else False
        c10 = c1 and c2 and c3

        if c10:
            fzero = 80; 
            deltaf = 80; 
            fend = 3000; 
            fbeats = numpy.array([]) # instantiate an empty numpy array
            pbeats = numpy.array([]) # instantiate an empty numpy array
            while fzero < fend:
                indx, frq_val = Common.list_search(frq, fzero, 0, 1e-3)
                fbeats = numpy.append(fbeats, frq_val) # append data to the numpy array
                pbeats = numpy.append(pbeats, power[indx]) # append data to the numpy array
                #print(indx,',',frq_val,',',power[indx])
                fzero = fzero + deltaf
            return [fbeats, pbeats]
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nInput Arrays Incorrectly Sized'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Estimate_No_Viable_Peaks(pbeats, CNR_min, Noise_level):

    # Estime the no. of real peaks in a given trace
    # from the power at each beat signal
    # If pbeat - pmin > CNR_min then the peak is considered real
    # R. Sheehan 25 - 11 - 2022

    FUNC_NAME = ".Estimate_No_Viable_Peaks()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if math.fabs(Noise_level) > 0 else False
        c2 = True if len(pbeats) > 0 else False
        c3 = True if CNR_min > 0 else False
        c10 = c1 and c2 and c3

        if c10:
            count = 0
            for i in range(0, len(pbeats), 1):
                if pbeats[i] - Noise_level > CNR_min: count = count + 1
            return count
        else:
            ERR_STATEMENT = ERR_STATEMENT + "Incorrect input arguments\n"
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Estimate_SNR(frq, power, sig_range):
    # use the measured data to estimate the SNR
    # signal = power within sig_range
    # noise = power outside sig_range
    # R. Sheehan 11 - 11 - 2022

    FUNC_NAME = ".Estimate_SNR()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if len(frq) > 0 else False
        c2 = True if len(power) > 0 else False
        c3 = True if len(frq) == len(power) else False
        c4 = True if sig_range[0] > frq[0] and sig_range[-1] < frq[-1] else False
        c10 = c1 and c2 and c3 and c4

        if c10:
            signal = 0 # integrate over the sig_range 
            noise = 0 # everything else is noise
            deltaf = 0
            for i in range(1, len(frq), 1):
                deltaf = frq[i] - frq[i-1]
                if frq[i] > sig_range[0] and frq[i] <= sig_range[1]:
                    signal = signal + power[i]
                else:
                    noise = noise + power[i]        
            signal  = signal * deltaf / 1000.0 # divide by 1000 just to scale
            noise = noise * deltaf / 1000.0 # divide by 1000 just to scale
            SNR = signal - noise if math.fabs(noise) > 0 else 0.0
            return [signal, noise, SNR]
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nInput Arrays Incorrectly Sized'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Measured_SNR():

    # Make a plot of the measured SNR data obtained from ESA
    # R. Sheehan 15 - 11 - 2022

    FUNC_NAME = ".Estimate_SNR()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_1310/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            PLOT_CNR_VOA = False

            if PLOT_CNR_VOA:            
                Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]
                CNR15 = [14.95, 14.95, 15.65, 19.36, 20.17, 20.38, 20.37, 20.29, 20.25, 20.18, 19.57]
                deltaCNR15 = [0.7170, 0.7915, 0.9465, 0.9620, 1.1505, 0.9950, 0.9780, 0.9340, 0.7675, 0.9900, 0.9920]
                CNR20 = [14.61, 14.64, 15.10, 20.12, 21.94, 22.69, 22.74, 22.78, 22.77, 22.61, 21.66]
                deltaCNR20 = [0.8570, 0.8800, 0.8370, 0.9520, 1.2910, 1.0825, 1.1425, 0.8365, 1.0145, 1.2870, 0.8490]

                filename = 'CNR_Bias_BW_5_Off_20_RBW_20k.txt'
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
            
                hv_data = []; labels = []; marks = []; 
                hv_data.append([Vvolts, CNR15, deltaCNR15]); labels.append(r'$\Delta$ = 15 MHz'); marks.append(Plotting.labs_pts[0])
                hv_data.append([Vvolts, CNR20, deltaCNR20]); labels.append(r'$\Delta$ = 20 MHz'); marks.append(Plotting.labs_pts[1])
                hv_data.append(data); labels.append(r'Sweep $\Delta$ = 20 MHz'); marks.append(Plotting.labs_pts[2])

                # Plot the data
                args = Plotting.plot_arg_multiple()
                
                # Extended LL Plot
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'VOA Bias / V'
                args.y_label = 'CNR / dBm / 20kHz'
                args.plt_range = [-0.2, 4.2, 12, 25]
                args.fig_name = 'Measured_CNR'

                Plotting.plot_multiple_curves_with_errors(hv_data, args)

            PLOT_CNR_SINGLE = True

            if PLOT_CNR_SINGLE:
                filename = 'LD5_591_CNR_VOA_Bias.txt'
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 

                # Plot the data
                args = Plotting.plot_arg_single()
                
                # Extended LL Plot
                args.loud = True
                #args.curve_label = labels
                #args.mrk_list = marks
                args.x_label = 'VOA Bias / V'
                args.y_label = 'CNR / dBm / 20kHz'
                #args.plt_range = [-0.2, 4.2, 12, 25]
                args.fig_name = 'Measured_CNR'

                Plotting.plot_single_curve_with_errors(data[0], data[1], data[2], args)

            Plot_CNR_Beats = False

            if Plot_CNR_Beats:
                filename = 'CNR_Beat_Frq_VOA_35.txt'
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True);

                D = 50; # length of fibre used in LCR-DSHI loop
                distance = numpy.arange(D, 21*D, D)

                print('len(data[0])',len(data[0]))
                print('len(distance)',len(distance))
                
                # Plot the data
                args = Plotting.plot_arg_single()

                xdistance = True
                
                # Extended LL Plot
                args.loud = True
                args.curve_label = ''
                args.marker = Plotting.labs_pts[1]
                args.x_label = 'Beat Frequency / MHz' if xdistance is False else 'Effective Loop Length / km'
                args.y_label = 'CNR / dBm / 20kHz'
                #args.plt_range = [-0.2, 4.2, 12, 25]
                args.fig_name = filename.replace('.txt','' if xdistance is False else '_Distance')

                #Plotting.plot_single_curve_with_errors(data[0], data[1], data[2], args)
                Plotting.plot_single_linear_fit_curve_with_errors(distance, data[1], data[2], args)
                #Plotting.plot_single_linear_fit_curve(data[0], data[1], args)f

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Spectra():

    # Need a generic method for plotting spectra
    # Edit this when you want to plot spectra
    # R. Sheehan 18 - 11 - 2022

    FUNC_NAME = ".Plot_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_Setup_Test/'
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_1310/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            #BeatFrqs = [80, 160, 320, 640, 1280]
            BeatFrqs = numpy.arange(80, 700, 80)

            Voltsstr = [250, 300, 350, 400, 450]
            Volts = numpy.arange(2.5, 4.7, 0.5)

            #filetmplt = 'Spctrm_%(v1)d_VOA_35.txt'
            #filetmplt = 'LD5_591_Spctrm_350_f_%(v1)d.txt'
            filetmplt = 'LD5_591_Spctrm_%(v1)s_f_80.txt'

            # Import the data
            hv_data = []
            labels = []
            marks = []
            
            SUBTRACT_OFFSET = False

            SINGLE_PLOTS = False

            PLOT_VOA = True

            val_lst = BeatFrqs if PLOT_VOA is False else Voltsstr

            for ss in range(0, len(val_lst), 1): 
                filename = filetmplt%{"v1":val_lst[ss]}
                if glob.glob(filename):
                    data = numpy.loadtxt(filename, unpack = True)

                    if SUBTRACT_OFFSET: data[0] = data[0] - BeatFrqs[ss]
                    
                    # Gather the data together for a combined plot
                    hv_data.append(data)
                    
                    the_label = 'f$_{b}$ = %(v1)d MHz'%{"v1":val_lst[ss]} if PLOT_VOA is False else 'V$_{VOA}$ = %(v1)0.1f V'%{"v1":Volts[ss]}

                    labels.append(the_label)

                    marks.append(Plotting.labs_lins[ss%len(Plotting.labs_lins)])

                    # Plot the data as it comes in
                    if SINGLE_PLOTS:
                        args = Plotting.plot_arg_single()
                
                        args.loud = False
                        args.curve_label = the_label
                        args.marker = Plotting.labs_lins[0]
                        args.x_label = 'Frequency ( MHz )'
                        args.y_label = 'Spectral Power ( dBm / 20kHz )'
                        args.plt_range = [30, 130, -95, -50]
                        args.fig_name = filename.replace('.txt','')
            
                        Plotting.plot_single_curve(data[0], data[1], args)

            COMBINED_PLOT = True

            if COMBINED_PLOT:
                # Plot the data
                args = Plotting.plot_arg_multiple()
                
                # Extended LL Plot
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm / 20kHz )'
                args.plt_range = [30, 130, -95, -50]
                #args.fig_name = 'Spectrum_Beat_Frq_Offset' if SUBTRACT_OFFSET else  'Spectrum_Beat_Frq'
                args.fig_name = 'Spectrum_VOA_Bias'
            
                Plotting.plot_multiple_curves(hv_data, args)

            del hv_data; del labels; del marks; 
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_LLM_Analysis(DATA_HOME, RBW_Val = 500, Tmeas = 20, theXUnits = 'kHz', theYUnits = 'Hz', Deff = 400, Pin = 0, VVOA = 3.5):

    # Generate all the plots from the Multi-LLM Measurements
    # R. Sheehan 21 - 11 - 2022

    # The axes
    # 0: Time / s
    # 1: Tair / C
    # 2: Taom / C
    # 3: Taomdrv / C
    # 4: Pmax / dBm
    # 5: Fmax / (MHz or kHz) Fmax < 80 =. kHz
    # 6: LLest@-3dB / (MHz or kHz) Fmax < 80 =. kHz
    # 7: LLVfit / (MHz or kHz) Fmax < 80 =. kHz
    # 8: LLLfit / (MHz or kHz) Fmax < 80 =. kHz
    # 9: LL@-20dB / (MHz or kHz) Fmax < 80 =. kHz
    # 10: V_{h} / "nW"
    # 11: V_{c} / (MHz or kHz) Fmax < 80 =. kHz
    # 12: V_{\gamma} / (MHz or kHz) Fmax < 80 =. kHz
    # 13: V_{\sigma} / (MHz or kHz) Fmax < 80 =. kHz
    # 14: L_{h} / "nW"
    # 15: L_{c} / (MHz or kHz) Fmax < 80 =. kHz
    # 16: L_{\sigma} / (MHz or kHz) Fmax < 80 =. kHz
    # 17: P_{1} / dBm
    # 18: P_{2} / dBm
    # 19: P_{2} / P_{1}

    FUNC_NAME = ".Multi_LLM_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_Setup_Test/LCR_DSHI_JDSU_DFB_T_20_D_50/'
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_1310/LCR_DSHI_LD5_591_T_25_D_10/'
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_400/LLM_Data_Nmeas_200_I_100_19_06_2023_19_06/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # for now work on a single file, then make it more generic
            #thefile = 'LLM_Data_Nmeas_10_I_50_16_11_2022_12_53.txt'
            #thefile = 'LLM_Data_Nmeas_100_I_50_16_11_2022_13_02.txt'
            #thefile = 'LLM_Data_Nmeas_50_I_25_07_12_2022_15_01.txt'
            
            #thefile = 'LLM_Data_Nmeas_100_I_100_29_03_2023_12_02.txt'
            #thefile = 'LLM_Data_Nmeas_100_I_100_30_03_2023_10_17.txt'
            #thefile = 'LLM_Data_Nmeas_100_I_100_30_03_2023_11_17.txt'
            #thefile = 'LLM_Data_Nmeas_100_I_100_30_03_2023_12_03.txt'
            #thefile = 'LLM_Data_Nmeas_100_I_100_30_03_2023_12_51.txt'
            #thefile = 'LLM_Data_Nmeas_100_I_100_30_03_2023_13_27.txt'
            #thefile = 'LLM_Data_Nmeas_200_I_300_05_04_2023_16_15.txt'

            #theDir = 'LLM_Data_Nmeas_200_I_100_19_06_2023_19_06/'

            thefile = 'Multi_LLM_Data.txt'

            if glob.glob(thefile):

                print("Analysing: ",thefile)

                # read the data from the file
                data = pandas.read_csv(thefile, delimiter = '\t')
                titles = list(data)

                #print(titles, ", len(titles) = ", len(titles), ", len(data) = ", data.shape[1])
                #print('')

                LOUD = True
                ERRORISSTDEV = True
                INCLUDEFIT = True

                # Start publilshing the results
                #if not glob.glob('ResultsSummary.txt'): 
                
                Multi_LLM_Fit_Params_Report(data, titles, ERRORISSTDEV, LOUD)

                LOUD = False      
                
                # Perform Correlation calculations of the variables
                RUN_CORRELATIONS = True

                # No need to check this, T_{AOM} is constant
                RUN_TAOM_CORRELATIONS = RUN_PMAX_CORRELATIONS = RUN_LLEST_CORRELATIONS = True

                if RUN_CORRELATIONS:
                    # Correlations with Time
                    axis_n = 0; 
                    axes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19]
                    INCLUDEHIST = True
                    for axis_m in axes:
                        Multi_LLM_Correlation(data, titles, axis_n, axis_m, INCLUDEHIST, ERRORISSTDEV, LOUD)

                    # Correlations with Pmax
                    if RUN_PMAX_CORRELATIONS:
                        axis_n = 4
                        axes = [6, 7, 8, 9, 10, 14, 17, 18]
                        INCLUDEHIST = False
                        for axis_m in axes:
                            Multi_LLM_Correlation(data, titles, axis_n, axis_m, INCLUDEHIST, ERRORISSTDEV, LOUD)

                    # Correlations with AOM-Temperature
                    # T_{AOM} = constant, no need to check for correlations here
                    if RUN_TAOM_CORRELATIONS:
                        axis_n = 2
                        axes = [6, 7, 8, 9, 10, 14, 17, 18]
                        for axis_m in axes:
                            Multi_LLM_Correlation(data, titles, axis_n, axis_m, INCLUDEHIST, ERRORISSTDEV, LOUD)

                    # Correlations with LL-Est
                    if RUN_LLEST_CORRELATIONS:
                        axis_n = 6
                        axes = [7, 8, 9, 17, 18]
                        for axis_m in axes:
                            Multi_LLM_Correlation(data, titles, axis_n, axis_m, INCLUDEHIST, ERRORISSTDEV, LOUD)

                        # Correlation of LL-Vfit with LL-Lfit
                        axis_n = 7
                        axis_m = 8
                        Multi_LLM_Correlation(data, titles, axis_n, axis_m, INCLUDEHIST, ERRORISSTDEV, LOUD)

                RUN_LINESHAPE_PLOT_COMPUTATION = True

                if RUN_LINESHAPE_PLOT_COMPUTATION:
                    # Make a plot of the spectra with max/min fitted params
                    Plot_Fitted_Lineshape_with_Data(data, titles, RBW_Val, Tmeas, theXUnits, theYUnits, Deff, Pin, VVOA, ERRORISSTDEV, INCLUDEFIT, LOUD)
                
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_LLM_Correlation(dataFrame, titles, axis_n, axis_m, include_hist = True, errorIsstdev = True, loud = False):

    # Perform correlation analysis on two columns of the Multi-LLM data
    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
    # errorIsstdev decides whether or not you want the error to be expressed in terms of the standard deviation or the data range
    # axis_n is one parameter of the correlation
    # axis_m is the other parameter of the correlation, in some cases this will be a dependent variable
    # R. Sheehan 21 - 11 - 2022

    FUNC_NAME = ".Multi_LLM_Correlation()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if dataFrame.empty:
            ERR_STATEMENT = ERR_STATEMENT + '\ndataFrame is empty\n'
            raise Exception
        else:
            if titles is None: titles = list(dataFrame)

            # Do the correlation calculations
            average = dataFrame[titles[axis_m]].mean()
            stdev = dataFrame[titles[axis_m]].std()
            maxval = dataFrame[titles[axis_m]].max()
            minval = dataFrame[titles[axis_m]].min()
            errorRange = 0.5*( math.fabs(maxval) - math.fabs(minval) )
            KK = dataFrame[ titles[axis_m] ].kurt() # compute the kurtosis of the distribution
            rcoeff = dataFrame[ titles[axis_m] ].corr(dataFrame[ titles[axis_n] ])
            #LLrcoeff = numpy.corrcoef( numpy.asarray( dataFrame[ titles[axis_n] ] ), numpy.asarray( dataFrame[ titles[axis_m] ] ) ) # compute the correlation coefficient for the data pair                        

            # make a basic linear fit plot
            args = Plotting.plot_arg_single()

            # Plot the Time Series of axis_m
            args.loud = loud
            args.x_label = titles[axis_n]
            args.y_label = titles[axis_m]
            args.plt_title = '%(v1)s %(v2)0.3f +/- %(v3)0.3f, r = %(v4)0.3f'%{"v1":titles[axis_m], "v2":average, "v3":(stdev if errorIsstdev else errorRange), "v4":rcoeff}
            args.fig_name = '%(v1)s_vs_%(v2)s'%{"v1":titles[axis_m].replace('/','_'), "v2":titles[axis_n].replace('/','_')}            
            Plotting.plot_single_linear_fit_curve( dataFrame[ titles[axis_n] ], dataFrame[ titles[axis_m] ], args )

            if include_hist:
                # Plot the Histogram of axis_m
                args.x_label = titles[axis_m]
                args.y_label = 'Frequency'
                #args.plt_title = '%(v1)s %(v2)0.3f +/- %(v3)0.3f, K = %(v4)0.3f'%{"v1":titles[axis_m], "v2":average, "v3":(stdev if errorIsstdev else errorRange), "v4":KK}
                args.plt_title = '%(v1)s %(v2)0.3f +/- %(v3)0.3f'%{"v1":titles[axis_m], "v2":average, "v3":(stdev if errorIsstdev else errorRange)}
                args.fig_name = 'Histogram_%(v1)s'%{"v1":titles[axis_m].replace('/','_')}
                Plotting.plot_histogram(dataFrame[ titles[axis_m] ], args)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_LLM_Extract_Fit_Params_Old_Deprecated(dataFrame, titles, errorIsstdev = True, loud = False):

    # DO NOT USE!!!!
    # Code Deprecated New Version Improved Version Available
    # R. Sheehan 24 - 1 - 2024

    # Extract the average of the fitted model parameters from the Multi-LLM data
    # Make a plot showing the model with the average, max, min fitted parameters
    # Use this to estimate LLM at both 3dB and 20dB levels
    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
    # errorIsstdev decides whether or not you want the error to be expressed in terms of the standard deviation or the data range
    # Voigt = True => Plot Voigt model
    # Voigt = False => Plot Lorentz Model
    # Use C++ dll to compute model values
    # LLest = 6, LLVfit = 7, LLLfit = 8
    # Voigt params V_{h} = 10, f_{0} = 11, V_{g} = 12, V_{s} = 13
    # Lorentz params L_{h} = 14, f_{0} = 15, L_{g} = 16
    # R. Sheehan 21 - 11 - 2022

    # I think this needs some work,  what exactly is going on here? 
    # How does the computed average fit compare with the measured data? 
    # R. Sheehan 22 - 1 - 2024

    FUNC_NAME = ".Multi_LLM_Extract_Fit_Params_Old_Deprecated()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        ATTEMPTING_TO_USE = True
        if ATTEMPTING_TO_USE:
            ERR_STATEMENT = ERR_STATEMENT + '\nDO NOT USE!!!\nThis version of the code has been deprecated\n'
            raise Exception
        elif dataFrame.empty:
            ERR_STATEMENT = ERR_STATEMENT + '\ndataFrame is empty\n'
            raise Exception
        else:
            if titles is None: titles = list(dataFrame)

            flow = 639; fhigh = 641; Nsteps = 500; 
            plt_rng = '%(v1)d %(v2)d %(v3)d'%{"v1":flow, "v2":fhigh, "v3":Nsteps}

            # Averaged Voigt Model Fit Parameters
            Vh = columnStatistics(dataFrame, titles, 10, errorIsstdev) # fitted height
            Vf0 = columnStatistics(dataFrame, titles, 11, errorIsstdev) # centre frequency
            Vgamma = columnStatistics(dataFrame, titles, 12, errorIsstdev) # Lorentzian HWHM
            Vsigma = columnStatistics(dataFrame, titles, 13, errorIsstdev) # Gaussian std. dev.

            # generate the arg-val strings
            Vave = '%(v1)0.5f %(v2)0.5f %(v3)0.5f %(v4)0.5f'%{"v1":Vh['Average'], "v2":Vf0['Average'], 
                                                              "v3":Vgamma['Average'], "v4":Vsigma['Average']}
            Vavefile = 'Voigt_Average.txt'
            Vaveargs = Vave + ' ' + plt_rng + ' ' + Vavefile

            Vmax = '%(v1)0.5f %(v2)0.5f %(v3)0.5f %(v4)0.5f'%{"v1":Vh['Max'], "v2":Vf0['Average'], 
                                                              "v3":Vgamma['Max'], "v4":Vsigma['Max']}
            Vmaxfile = 'Voigt_Max.txt'
            Vmaxargs = Vmax + ' ' + plt_rng + ' ' + Vmaxfile

            Vmin = '%(v1)0.5f %(v2)0.5f %(v3)0.5f %(v4)0.5f'%{"v1":Vh['Min'], "v2":Vf0['Average'], 
                                                              "v3":Vgamma['Min'], "v4":Vsigma['Min']}
            Vminfile = 'Voigt_Min.txt'
            Vminargs = Vmin + ' ' + plt_rng + ' ' + Vminfile

            # Averaged Lorentz Model Fit Parameters
            Lh = columnStatistics(dataFrame, titles, 14, errorIsstdev) # fitted height
            Lf0 = columnStatistics(dataFrame, titles, 15, errorIsstdev) # centre frequency
            Lgamma = columnStatistics(dataFrame, titles, 16, errorIsstdev) # Lorentzian HWHM

            # generate the arg-val strings
            Lave = '%(v1)0.5f %(v2)0.5f %(v3)0.5f'%{"v1":Lh['Average'], "v2":Lf0['Average'], "v3":Lgamma['Average']}
            Lavefile = 'Lorentz_Average.txt'
            Laveargs = Lave + ' ' + plt_rng + ' ' + Lavefile

            Lmax = '%(v1)0.5f %(v2)0.5f %(v3)0.5f'%{"v1":Lh['Max'], "v2":Lf0['Average'], "v3":Lgamma['Max']}
            Lmaxfile = 'Lorentz_Max.txt'
            Lmaxargs = Lmax + ' ' + plt_rng + ' ' + Lmaxfile

            Lmin = '%(v1)0.5f %(v2)0.5f %(v3)0.5f'%{"v1":Lh['Min'], "v2":Lf0['Average'], "v3":Lgamma['Min']}
            Lminfile = 'Lorentz_Min.txt'
            Lminargs = Lmin + ' ' + plt_rng + ' ' + Lminfile

            PLOT_IN_DBM = True

            # Call the executable with ave, max, min params to generate data            
            # Import the data and make the plot
            hv_data = []; labels = []; marks = [];

            Compute_Spectrum(True, Vaveargs)
            spctr_data = numpy.loadtxt(Vavefile, delimiter = ',', unpack = True)
            if PLOT_IN_DBM:
                spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
            hv_data.append(spctr_data); labels.append('V$_{ave}$'); marks.append(Plotting.labs_lins[0])

            Compute_Spectrum(True, Vmaxargs)
            spctr_data = numpy.loadtxt(Vmaxfile, delimiter = ',', unpack = True)            
            if PLOT_IN_DBM:
                spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
            hv_data.append(spctr_data); labels.append('V$_{max}$'); marks.append(Plotting.labs_dotdash[0])

            Compute_Spectrum(True, Vminargs)
            spctr_data = numpy.loadtxt(Vminfile, delimiter = ',', unpack = True)            
            if PLOT_IN_DBM:
                spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
            hv_data.append(spctr_data); labels.append('V$_{min}$'); marks.append(Plotting.labs_dotted[0])

            Compute_Spectrum(False, Laveargs)
            spctr_data = numpy.loadtxt(Lavefile, delimiter = ',', unpack = True)            
            if PLOT_IN_DBM:
                spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
            hv_data.append(spctr_data); labels.append('L$_{ave}$'); marks.append(Plotting.labs_lins[1])

            Compute_Spectrum(False, Lmaxargs)
            spctr_data = numpy.loadtxt(Lmaxfile, delimiter = ',', unpack = True)            
            if PLOT_IN_DBM:
                spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
            hv_data.append(spctr_data); labels.append('L$_{max}$'); marks.append(Plotting.labs_dotdash[1])

            Compute_Spectrum(False, Lminargs)
            if glob.glob(Lminfile):
                spctr_data = numpy.loadtxt(Lminfile, delimiter = ',', unpack = True)            
                if PLOT_IN_DBM:
                    spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                    spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
                hv_data.append(spctr_data); labels.append('L$_{min}$'); marks.append(Plotting.labs_dotted[1])

            # Plot the data
            args = Plotting.plot_arg_multiple()
                
            # Extended LL Plot
            args.loud = loud
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency ( kHz )'
            #args.y_label = 'Spectral Power ( dBm / 20kHz )' if PLOT_IN_DBM else 'Spectral Power ( nW / 20kHz )'
            args.y_label = 'Spectral Power ( dBm / 500Hz )' if PLOT_IN_DBM else 'Spectral Power ( nW / 500Hz )'
            #args.plt_range = [30, 130, -105, -70]
            #args.fig_name = 'Voigt_Spectrum'
            #args.fig_name = 'Lorentz_Spectrum'
            args.fig_name = 'Fitted_Spectrum_dBm' if PLOT_IN_DBM else 'Fitted_Spectrum_nW'

            Plotting.plot_multiple_curves(hv_data, args)

            # Extended LL Plot
            args.loud = loud
            args.crv_lab_list = labels[0:3]
            args.mrk_list = marks[0:3]
            args.x_label = 'Frequency ( kHz )'
            #args.y_label = 'Spectral Power ( dBm / 20kHz )' if PLOT_IN_DBM else 'Spectral Power ( nW / 20kHz )'
            args.y_label = 'Spectral Power ( dBm / 500Hz )' if PLOT_IN_DBM else 'Spectral Power ( nW / 500Hz )'
            #args.plt_range = [30, 130, -105, -70]
            #args.fig_name = 'Voigt_Spectrum'
            #args.fig_name = 'Lorentz_Spectrum'
            args.fig_name = 'Fitted_Voigt_Spectrum_dBm' if PLOT_IN_DBM else 'Fitted_Voigt_Spectrum_nW'

            Plotting.plot_multiple_curves(hv_data[0:3], args)

            # Extended LL Plot
            args.loud = loud
            args.crv_lab_list = labels[3:6]
            args.mrk_list = marks[3:6]
            args.x_label = 'Frequency ( kHz )'
            #args.y_label = 'Spectral Power ( dBm / 20kHz )' if PLOT_IN_DBM else 'Spectral Power ( nW / 20kHz )'
            args.y_label = 'Spectral Power ( dBm / 500Hz )' if PLOT_IN_DBM else 'Spectral Power ( nW / 500Hz )'
            #args.plt_range = [30, 130, -105, -70]
            #args.fig_name = 'Voigt_Spectrum'
            #args.fig_name = 'Lorentz_Spectrum'
            args.fig_name = 'Fitted_Lorentz_Spectrum_dBm' if PLOT_IN_DBM else 'Fitted_Lorentz_Spectrum_nW'

            Plotting.plot_multiple_curves(hv_data[3:6], args)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Fitted_Lineshape_with_Data(dataFrame, titles, RBW_Val = 500, Tmeas = 20, theXUnits = 'kHz', theYUnits = 'Hz', Deff = 400, Pin = 0, VVOA = 3.5, errorIsstdev = True, AddFitted = False, loud = False):

    # Extract the average of the fitted model parameters from the Multi-LLM data
    # Make a plot showing the model with the average fitted parameters along with the measured data

    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
    # RBW_Val is the value of the resolution BW used to perform the measurement
    # Tmeas is the approximate time that was needed to perform the measurement
    # theXunits are the Frequency units that you want displayed along the x-axis
    # theYUnits are the Frequency units of the RBW value that you want displayed along the y-axis
    # Deff is the effective loop length used to perform the measurement, units of km
    # Pin is the output power from the laser / input power to the LCR-DSHI loop, units of dBm
    # VVOA is the VOA bias that was applied at the time of the measurement, unit of V
    # errorIsstdev decides whether or not you want the error to be expressed in terms of the standard deviation or the data range
        
    # Use C++ executable to compute model values
    # Voigt = True => Plot Voigt model
    # Voigt = False => Plot Lorentz Model

    # LLest = 6, LLVfit = 7, LLLfit = 8 # axes of the dataFrame which may be of interest
    # Voigt params V_{h} = 10, f_{0} = 11, V_{g} = 12, V_{s} = 13
    # Lorentz params L_{h} = 14, f_{0} = 15, L_{g} = 16
    
    # R. Sheehan 21 - 11 - 2022

    # Updated R. Sheehan 24 - 1 - 2024
    # The updated method combines Multi_LLM_Extract_Fit_Params_Old_Deprecated with Plot_Multiple_Spectra_Old_Deprecated

    # Updated R. Sheehan 24 - 2 - 2024
    # Had to add an option on whether or not to include the fitted data because access restrictions mean that I can't call an external .exe file
    # AddFitted = False means that the fitted lineshape is not included in the plot that is generated by this method

    FUNC_NAME = ".Plot_Fitted_Lineshape_with_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if dataFrame.empty:
            ERR_STATEMENT = ERR_STATEMENT + '\ndataFrame is empty\n'
            raise Exception
        else:
            # Import the measured lineshape data
            LINESHAPE_DATA_EXISTS = False # If no measured LLM files exist then just plot the computed Voigt and Lorentz lineshapes together
            xlow = 0.0; xhigh = 0.0; # variables for storing the endpoints of the frequency plot range
            hv_data = []; marks = []; labels = []; # variables for storing imported data
            files = glob.glob('LLM_Meas_*.txt')
            if files:
                LINESHAPE_DATA_EXISTS = True
                files.sort(key=lambda f: int(re.sub(r'\D', '', f))) # sort the filenames in place using the number within the string, assumes single digit in string

                deltaT = Tmeas / 60.0 # measurement time in mins
                 
                #nskip = 8 # only plot every nskip measurements, NKT
                count_mrk = 0
                nskip = 5 # only plot every nskip measurements, CoBrite
                for i in range(0, len(files), nskip):
                    values = Common.extract_values_from_string(files[i])
                    theTime = float(values[0])*deltaT
                    data = numpy.loadtxt(files[i], delimiter = '\t')
                    if xlow == 0.0 and xhigh == 0.0:
                        xlow = data[0][0]; xhigh = data[0][-1];
                    hv_data.append(data); marks.append(Plotting.labs_dotted[count_mrk%len(Plotting.labs_dotted)]); labels.append('T = %(v1)0.1f mins'%{"v1":theTime})
                    #hv_data.append(data); marks.append(Plotting.labs_line_only[count_mrk%len(Plotting.labs_line_only)]); labels.append('T = %(v1)0.1f mins'%{"v1":theTime})
                    #hv_data.append(data); marks.append(Plotting.labs_mrk_only[count_mrk%len(Plotting.labs_mrk_only)]); #labels.append('T = %(v1)0.1f mins'%{"v1":theTime})
                    count_mrk = count_mrk + 1

            # Define the titles from the dataFrame
            if titles is None: titles = list(dataFrame)            

            # define the plot range string based on the endpoints of the measured data sets
            Nsteps = 500;

            plt_rng = '%(v1)d %(v2)d %(v3)d'%{"v1":xlow, "v2":xhigh, "v3":Nsteps}
            
            PLOT_IN_DBM = True # Always plot in dBm since the measured data is output in units of dBm
            
            # Call the executable with aveparams to generate data fitted Voigt and Lorentz lineshapes
            if AddFitted:
                # Averaged Voigt Model Fit Parameters
                Vh = columnStatistics(dataFrame, titles, 10, errorIsstdev) # fitted height
                Vf0 = columnStatistics(dataFrame, titles, 11, errorIsstdev) # centre frequency
                Vgamma = columnStatistics(dataFrame, titles, 12, errorIsstdev) # Lorentzian HWHM
                Vsigma = columnStatistics(dataFrame, titles, 13, errorIsstdev) # Gaussian std. dev.

                # In the event of no lineshape data being available just plot the lineshapes about the central frequency
                if LINESHAPE_DATA_EXISTS is False: 
                    xlow = Vf0['Average'] - 50
                    xhigh = Vf0['Average'] + 50
                    
                # generate the arg-val strings for the Voigt lineshape calculation
                Vave = '%(v1)0.5f %(v2)0.5f %(v3)0.5f %(v4)0.5f'%{"v1":Vh['Average'], "v2":Vf0['Average'], "v3":Vgamma['Average'], "v4":Vsigma['Average']}
                Vavefile = 'Voigt_Average.txt'
                Vaveargs = Vave + ' ' + plt_rng + ' ' + Vavefile
                
                # Compute the Voigt lineshape spectrum
                # Method Compute_Spectrum sends the computed data to the file named in the arg_string, in this case Vavefile
                Compute_Spectrum(True, Vaveargs)
                spctr_data = numpy.loadtxt(Vavefile, delimiter = ',', unpack = True)
                if PLOT_IN_DBM:
                    spctr_data[1] = spctr_data[1] / 1e+6 # convert nW -> mW
                    spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
                hv_data.append(spctr_data); labels.append('V$_{ave}$'); marks.append(Plotting.labs_lins[0])

                # Averaged Lorentz Model Fit Parameters
                Lh = columnStatistics(dataFrame, titles, 14, errorIsstdev) # fitted height
                Lf0 = columnStatistics(dataFrame, titles, 15, errorIsstdev) # centre frequency
                Lgamma = columnStatistics(dataFrame, titles, 16, errorIsstdev) # Lorentzian HWHM

                # generate the arg-val strings
                Lave = '%(v1)0.5f %(v2)0.5f %(v3)0.5f'%{"v1":Lh['Average'], "v2":Lf0['Average'], "v3":Lgamma['Average']}
                Lavefile = 'Lorentz_Average.txt'
                Laveargs = Lave + ' ' + plt_rng + ' ' + Lavefile

                # Compute the Lorentz lineshape spectrum
                # Method Compute_Spectrum sends the computed data to the file named in the arg_string, in this case Lavefile
                Compute_Spectrum(False, Laveargs)
                spctr_data = numpy.loadtxt(Lavefile, delimiter = ',', unpack = True)            
                if PLOT_IN_DBM:
                    spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                    spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
                hv_data.append(spctr_data); labels.append('L$_{ave}$'); marks.append(Plotting.labs_lins[1])
                
                del spctr_data;

            # make a plot of the measured lineshape data
            args = Plotting.plot_arg_multiple()

            args.loud = loud
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency / %(v1)s'%{"v1":theXUnits}
            args.y_label = 'Power / dBm / %(v1)d%(v2)s'%{"v1":RBW_Val, "v2":theYUnits}
            #args.plt_range = [xlow, xhigh, -65, -25]
            args.plt_range = [xlow, xhigh, -90, -25]
            args.fig_name = 'Measured_Spectra'
            args.plt_title = 'D$_{eff}$ = %(v1)d km, P$_{in}$ = %(v2)0.1f dBm, V$_{VOA}$ = %(v3)0.1f V'%{"v1":Deff, "v2":Pin, "v3":VVOA}

            Plotting.plot_multiple_curves(hv_data, args)

            del hv_data; del labels; del marks;  
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_LLM_Fit_Params_Report(dataFrame, titles, errorIsstdev = True, loud = False):

    # Extract the average of the fitted model parameters from the Multi-LLM data
    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
    # errorIsstdev decides whether or not you want the error to be expressed in terms of the standard deviation or the data range
    # LLest = 6, LLVfit = 7, LLLfit = 8
    # Voigt params V_{h} = 10, f_{0} = 11, V_{g} = 12, V_{s} = 13
    # Lorentz params L_{h} = 14, f_{0} = 15, L_{g} = 16
    # R. Sheehan 21 - 11 - 2022

    FUNC_NAME = ".Multi_LLM_Fit_Params_Report()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if dataFrame.empty:
            ERR_STATEMENT = ERR_STATEMENT + '\ndataFrame is empty\n'
            raise Exception
        else:
            if titles is None: titles = list(dataFrame)

            # Redirect the output to a file
            old_target, sys.stdout = sys.stdout, open('ResultsSummary.txt', 'w')

            Nmeas = dataFrame.shape[0]
            totalTime = dataFrame[titles[0]][Nmeas-1]
            singleTime = totalTime / (Nmeas-1)

            print("Main Result")
            print("No. Measurements: %(v1)d"%{"v1":Nmeas})
            print("Total Time Taken / min: %(v1)0.2f"%{"v1":totalTime/60.0})
            print("Average Time per Meas / sec: %(v1)0.2f\n"%{"v1":singleTime})
            columnStatistics(dataFrame, titles, 4, errorIsstdev, loud) # Pmax
            columnStatistics(dataFrame, titles, 6, errorIsstdev, loud) # LL estimate from data
            columnStatistics(dataFrame, titles, 7, errorIsstdev, loud) # LL from Voigt Fit
            columnStatistics(dataFrame, titles, 8, errorIsstdev, loud) # LL from Lorentz Fit
            columnStatistics(dataFrame, titles, 9, errorIsstdev, loud) # LL-20 estimate from data
            
            print("\nVoigt Fit Parameters") # Averaged Voigt Model Fit Parameters
            columnStatistics(dataFrame, titles, 10, errorIsstdev, loud) # fitted height
            columnStatistics(dataFrame, titles, 11, errorIsstdev, loud) # centre frequency
            columnStatistics(dataFrame, titles, 12, errorIsstdev, loud) # Lorentzian HWHM
            columnStatistics(dataFrame, titles, 13, errorIsstdev, loud) # Gaussian std. dev.
            
            print("\nLorentz Fit Parameters") # Averaged Lorentz Model Fit Parameters
            columnStatistics(dataFrame, titles, 14, errorIsstdev, loud) # fitted height
            columnStatistics(dataFrame, titles, 15, errorIsstdev, loud) # centre frequency
            columnStatistics(dataFrame, titles, 16, errorIsstdev, loud) # Lorentzian HWHM
            
            print("\nAOM Temperature Statistics") # AOM Temperature Statistics
            columnStatistics(dataFrame, titles, 1, errorIsstdev, loud) # Air Temperature
            columnStatistics(dataFrame, titles, 2, errorIsstdev, loud) # AOM Temperature
            columnStatistics(dataFrame, titles, 3, errorIsstdev, loud) # AOM Driver Temperature

            print("\nLoop Power Statistics") # Loop Power Statistics
            columnStatistics(dataFrame, titles, 17, errorIsstdev, loud) # Input Power @ P1
            columnStatistics(dataFrame, titles, 18, errorIsstdev, loud) # Loop Power @ P2
            columnStatistics(dataFrame, titles, 19, errorIsstdev, loud) # Power Ratio P2 / P1

            sys.stdout = old_target # return to the usual stdout

            #Dict = columnStatistics(dataFrame, titles, 6, True)
            #print(Dict['Name'],':',Dict['Average'],'+/-',Dict['Err'])
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def columnStatistics(dataFrame, titles, axisNo, errorIsstdev = True, loud = False):

    # extract the basic statistics from a given column / axis of data
    # dataFrame is the dataset being analysed
    # titles is the list of names of the items in the dataFrame
    # axisNo is the index of the column of data being analysed
    # errorIsstdev decides whether or not you want the error to be expressed in terms of the standard deviation or the data range
    # return a dictionary containing the data and a formatted string
    # R. Sheehan 21 - 11 - 2022

    FUNC_NAME = ".columnStatistics()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if dataFrame.empty:
            ERR_STATEMENT = ERR_STATEMENT + '\ndataFrame is empty\n'
            raise Exception
        else:
            if titles is None: titles = list(dataFrame)
            if axisNo > len(titles):
                ERR_STATEMENT = ERR_STATEMENT + '\nNo data in column:' + axisNo + '\n'
                raise Exception
            else:
                # Compute the statistics
                average = dataFrame[titles[axisNo]].mean()
                #stdev = math.sqrt( math.fabs( dataFrame[titles[axisNo]].var() ) )
                stdev = dataFrame[titles[axisNo]].std(ddof = 1)
                maxval = dataFrame[titles[axisNo]].max()
                minval = dataFrame[titles[axisNo]].min()
                errorRange = 0.5*( math.fabs(maxval) - math.fabs(minval) )
                relErr = 100*(stdev/average) if errorIsstdev else 100*(errorRange/average)

                # create the dictionary for storing the values
                labels = []; values = []; 
                labels.append('Name'); values.append(titles[axisNo]); 
                labels.append('Average'); values.append(average); 
                labels.append('StdDev'); values.append(stdev); 
                labels.append('Max'); values.append(maxval); 
                labels.append('Min'); values.append(minval); 
                labels.append('Err'); values.append(errorRange); 
                labels.append('Rel. Err.'); values.append(relErr); 
                
                resDict = dict( zip( labels, values ) ) # make the dictionary

                # form the string for printing the results
                resStr = '%(v1)s\tAve: %(v2)0.5f\tStdDev: %(v3)0.5f\tMax: %(v4)0.5f\tMin: %(v5)0.5f\tErr: %(v6)0.5f\tRel-Err: %(v7)0.5f'
                resStr = resStr%{"v1":titles[axisNo], "v2":average, "v3":stdev, "v4":maxval, "v5":minval, "v6":errorRange, "v7":relErr}
                
                if loud:print(resStr)

                return resDict
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def DLL_Hacking():

    # Attempt to call a DLL inside python
    # It can be done, but it's very difficult and for what I want to achieve it's easier to use subprocess to call an executable
    # The following can be used by someone with more patience to attempt the effort
    # https://lonami.dev/blog/ctypes-and-windows/
    # https://stackoverflow.com/questions/71374379/how-to-use-ctypes-with-windows
    # https://stackoverflow.com/questions/69307713/oserror-winerror-193-1-is-not-a-valid-win32-application-when-using-ctypes
    # https://stackoverflow.com/questions/252417/how-can-i-use-a-dll-file-from-python
    # https://docs.python.org/3/library/ctypes.html
    # https://stackoverflow.com/questions/59330863/cant-import-dll-module-in-python
    # https://www.codementor.io/@spyoungtech/how-to-use-dlls-com-objects-from-python-or-how-to-send-a-fax-with-python-192lmtt5p5
    # https://dev.to/petercour/call-dll-functions-from-python-jo4
    # If you're using 64bit python then you must be calling a 64bit dll!
    # R. Sheehan 21 - 11 - 2022

    FUNC_NAME = ".DLL_Hacking()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DLL_Home = 'C:/Users/robertsheehan/Programming/C++/Fitting/Non_Lin_Fit/x64/Release/'
        DLL_Name = 'Non_Lin_Fit.dll'
        full_path = DLL_Home + DLL_Name

        #os.add_dll_directory(DLL_Home)

        #os.chdir(DLL_Home)
        #print(os.getcwd())
        #print(glob.glob("*.dll"))

        #NLF = ctypes.WinDLL(full_path)
        NLF = ctypes.CDLL(full_path)

        #NLF.Testing()
        #print(NLF.Testing())

        print(NLF.Testing_Ret())
        
        #name = ctypes.util.find_library(DLL_Name)
        #lib = ctypes.cdll.LoadLibrary(full_path)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Compute_Spectrum(spctr_choice, arg_vals):

    # Call a C++ executable to compute the Voigt or Lorentz lineshape 
    # spctr_choice = True tells the program to call Voigt.exe or Lorentz.exe otherwise
    # arg_vals is the string input needed by the executable to compute the spectrum
    # arg_vals is string of the form: Voigt fh fc fs fg flow fhigh Nsteps filename to compute a VOIGT spectrum based on Voigt parameters fh fc fs fg 
    # arg_vals is string of the form: Lorentz fh fc fs flow fhigh Nsteps filename to compute a Lorentz spectrum based on Lorentz parameters fh fc fs
    
    # This is implemented in Multi_LLM_Extract_Fit_Params as follows
    #plt_rng = '%(v1)d %(v2)d %(v3)d'%{"v1":flow, "v2":fhigh, "v3":Nsteps} # set the plot range
    #Vave = '%(v1)0.5f %(v2)0.5f %(v3)0.5f %(v4)0.5f'%{"v1":Vh['Average'], "v2":Vf0['Average'], "v3":Vgamma['Average'], "v4":Vsigma['Average']} # set the lineshape parameter values
    #Vavefile = 'Voigt_Average.txt' # specify the filename where the computed lineshape will be stored
    #Vaveargs = Vave + ' ' + plt_rng + ' ' + Vavefile # string to be entered when calling the executable
    
    # Similary for Lorentz.exe
    #Lave = '%(v1)0.5f %(v2)0.5f %(v3)0.5f'%{"v1":Lh['Average'], "v2":Lf0['Average'], "v3":Lgamma['Average']} # set the lineshape parameter values
    #Lavefile = 'Lorentz_Average.txt' # specify the filename where the computed lineshape will be stored
    #Laveargs = Lave + ' ' + plt_rng + ' ' + Lavefile # string to be entered when calling the executable
    
    # Attempted to get Python to call a DLL but I couldn't get it to work
    # Much easier to get Python to call an executable
    # R. Sheehan 21 - 11 - 2022

    FUNC_NAME = ".Compute_Spectrum()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        V_dir = 'C:/Users/robertsheehan/Programming/C++/Fitting/Voigt/x64/Release/'
        V_exe = 'Voigt.exe '

        L_dir = 'C:/Users/robertsheehan/Programming/C++/Fitting/Lorentz/x64/Release/'
        L_exe = 'Lorentz.exe '

        if os.path.isdir(V_dir) and os.path.isdir(L_dir):
            DIR = V_dir if spctr_choice else L_dir
            EXE = V_exe if spctr_choice else L_exe

            args = DIR + EXE + arg_vals

            output = subprocess.call(args, stdin=None, stdout=None, stderr=None, shell=False)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate ' + V_dir
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate ' + L_dir
            ERR_STATEMENT = ERR_STATEMENT + '\nPlease ensure that Voigt.exe and Lorentz.exe have been compiled and are available on this computer\n'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Beat_Analysis():

    # Analyse the data obtained from a series of beat note scans
    # R. Sheehan 13 - 12 - 2022

    # The beat note measurement looks at the lineshape at each beat note
    # The CNR is estimated by examining the PSD peak and its location relative to the beat freq
    # If the lineshape is valid then a fit is attempted and the data are saved
    # The beat note scan is then repeated multiple times in order to build up some statistics

    FUNC_NAME = ".Beat_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Ival = 300
        loopLength = 10

        # CoBrite Parameters
        # theLaser = 'CoBriteTLS'
        # temperature = 25        
        # RBW = '5kHz' # RBW used in the measurement
        # LWUNits = ' / MHz / ' + RBW

        # NKT Parameters
        theLaser = 'NKT'
        temperature = 35        
        RBW = '100Hz' # RBW used in the measurement
        LWUNits = ' / kHz / ' + RBW

        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/I_%(v1)d/'%{"v1":Ival, "v2":theLaser, "v3":temperature, "v4":loopLength}

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())             
            
            beatfiles = glob.glob('Beat_Data_Nmeas_*_I_%(v1)d*.txt'%{"v1":Ival})

            Nbeats, Titles, averaged_data, delta_data = Aggregate_Data_From_Beat_Files(beatfiles)
            
            # write the aggregated data to a file
            # use numpy.savetxt, fucking sweet!
            # https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
            # The data is stored row-wise, but I want the output to match the format of the data from LabVIEW
            # so I'm going to export the transpose of the data along with the headers            
            header_str = ''
            n_titles = len(Titles)
            for i in range(0, n_titles, 1):
                if i == n_titles-1:
                    header_str = header_str + '%(v1)s'%{"v1":Titles[i]}
                else:
                    header_str = header_str + '%(v1)s\t'%{"v1":Titles[i]}
            
            filename = 'Averaged_Data_I_%(v1)d.txt'%{"v1":Ival}
            numpy.savetxt(filename, numpy.transpose(averaged_data), fmt = '%0.9f', delimiter = '\t', header = header_str)

            filename = 'Delta_Data_I_%(v1)d.txt'%{"v1":Ival}
            numpy.savetxt(filename, numpy.transpose(delta_data), fmt = '%0.9f', delimiter = '\t', header = header_str)

            filename = 'Results_Summary_I_%(v1)d.txt'%{"v1":Ival}
            f_AOM = 80
            f_start = 240; # it may be necessary to skip the first beat due to bad fitting
            f_cutoff = (9) * f_AOM;
            Beat_Data_Report(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, averaged_data, delta_data, filename)

            Plot_Beat_Data(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, averaged_data, delta_data)
            
            # Data is returned as a numpy array with the measured quantities stored as rows of the array as follows
            # 0: Beat No.   1: Fbeat / MHz  2: Distance / km    3: Time/ s  4: Tair/C   5: Taom/C   6: Taomdrv/C    7: Pmax/dBm 8: Fmax	
            # 9: LLest	10: LL_Vfit	11: LL_Lfit	12: LLest_-20	13: Voigt_h/nW	14: Voigt_Lor_HWHM	15: Voigt_Gau_Stdev	16: Lor_h/nW	
            # 17: Lor_HWHM 18: P1/dBm	19: P2/dBm	20: P2/P1

            Loud = False
            Choices = [4, 5, 6] # Plot the temperatures together
            TheName = 'Temperature'
            TheUnits = ' / C'
            Plot_Beat_Data_Combo(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, Choices, TheName, TheUnits, averaged_data, delta_data, Loud)

            Loud = False
            Choices = [18, 19] # Plot the loop powers together
            TheName = 'Power'
            TheUnits = ' / dBm'
            Plot_Beat_Data_Combo(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, Choices, TheName, TheUnits, averaged_data, delta_data, Loud)

            Loud = True
            Choices = [9, 10, 11] # Plot the measured + fitted dnu together
            TheName = 'Linewidth'
            TheUnits = LWUNits
            Plot_Beat_Data_Combo(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, Choices, TheName, TheUnits, averaged_data, delta_data, Loud)

            Loud = False
            Choices = [9, 12] # Plot the estimated dnu together
            TheName = 'Estimated Linewidth'
            TheUnits = LWUNits
            Plot_Beat_Data_Combo(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, Choices, TheName, TheUnits, averaged_data, delta_data, Loud)

            Loud = True
            Choices = [14, 15] # Plot the Voigt Fit Parameters together
            TheName = 'Voigt Parameters'
            TheUnits = LWUNits
            Plot_Beat_Data_Combo(Nbeats, f_AOM, loopLength, f_start, f_cutoff, Titles, Choices, TheName, TheUnits, averaged_data, delta_data, Loud)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Summarise_Beat_Analysis():

    # Make plots comparing the measured beat results from different measurements
    # R. Sheehan 12 - 2 - 2024

    FUNC_NAME = ".Summarise_Beat_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        loopLength = 50

        # CoBrite Parameters
        #theLaser = 'CoBriteTLS'
        #temperature = 25        
        #RBW = '5kHz' # RBW used in the measurement
        #LWUNits = ' / MHz / ' + RBW
        #Pvals = [4.503, 5.478, 6.533]
        #Dstr = 'Distance / km'
        #LLstr = 'LL_Vfit/MHz'

        # NKT Parameters
        theLaser = 'NKT'
        temperature = 35        
        RBW = '100Hz' # RBW used in the measurement
        LWUNits = ' / kHz / ' + RBW
        Pvals = [3.217, 9.217, 11.682]
        Dstr = 'Distance / km'
        LLstr = 'LL_Vfit/kHz'

        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/I_%(v1)d/'%{"v1":Ival, "v2":theLaser, "v3":temperature, "v4":loopLength}
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/'%{"v2":theLaser, "v3":temperature, "v4":loopLength}

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Make a directory for storing the comparison plots
            resDir = 'Comparisons/'
            if not os.path.isdir(resDir): os.mkdir(resDir)

            hv_data = []; marks = []; labels = []; 

            EXTRACT_DATA = False
            if EXTRACT_DATA:
                # Extract the data from each of the summarised beat files
                Ivals = [100, 200, 300]                
                count = 0
                indx_start = 0; 
                indx_end = 16; 
                f_AOM = 80
                f_start = 80; # it may be necessary to skip the first beat due to bad fitting
                f_cutoff = (16) * f_AOM;
                for i in range(0, len(Ivals), 1):
                    data_dir = 'I_%(v1)d/'%{"v1":Ivals[i]}
                    if os.path.isdir(data_dir):
                        os.chdir(data_dir)
                        print(os.getcwd())
                        # Grab the averaged data
                        beatfile = 'Averaged_Data_I_%(v1)d.txt'%{"v1":Ivals[i]}
                        df = pandas.read_csv(beatfile, delimiter = '\t')
                        titles = list(df)

                        # Grab the error data
                        errorfile = 'Delta_Data_I_%(v1)d.txt'%{"v1":Ivals[i]}
                        delta_df = pandas.read_csv(errorfile, delimiter = '\t')

                        # store the data
                        xdata = df[ Dstr ].to_numpy()
                        ydata = df[ LLstr ].to_numpy()
                        deltaydata = delta_df[ LLstr ].to_numpy()

                        hv_data.append([ xdata[indx_start:indx_end], ydata[indx_start:indx_end], deltaydata[indx_start:indx_end] ] )
                        marks.append(Plotting.labs_pts[count%(len(Plotting.labs_pts))])
                        labels.append('P$_{in}$ = %(v1)0.2f dBm'%{"v1":Pvals[i]})

                        # dump the data
                        del df; del delta_df; del titles; del xdata; del ydata; del deltaydata; 

                        count = count + 1
                        os.chdir(DATA_HOME)
            
                print(os.getcwd())
                os.chdir(resDir)
                print(os.getcwd())

            WRITE_DATA = False
            if WRITE_DATA:
                # write the combined data set to a file
                the_avg_filename = 'Averaged_Data_D_%(v1)d.txt'%{"v1":loopLength}
                the_err_filename = 'Delta_Data_D_%(v1)d.txt'%{"v1":loopLength}

                the_avg_file = open(the_avg_filename,'w')
                the_avg_file.write('%(v1)s\t%(v2)s\t%(v2)s\t%(v2)s\n'%{"v1":Dstr, "v2":LLstr})
                the_avg_file.close()
                
                the_err_file = open(the_err_filename,'w')
                the_err_file.write('%(v1)s\t%(v2)s\t%(v2)s\t%(v2)s\n'%{"v1":Dstr, "v2":LLstr})
                the_err_file.close()

                the_avg_file = open(the_avg_filename,'a')
                the_err_file = open(the_err_filename,'a')

                if loopLength == 10:
                    for i in range(0, len(hv_data[0][0]), 1):
                        the_avg_file.write('%(v1)0.2f\t%(v2)0.9f\t%(v3)0.9f\t%(v4)0.9f\n'%{"v1":hv_data[0][0][i], "v2":hv_data[0][1][i], "v3":hv_data[1][1][i] if i<13 else 0.0, "v4":hv_data[2][1][i] if i<11 else 0.0 })
                        the_err_file.write('%(v1)0.2f\t%(v2)0.9f\t%(v3)0.9f\t%(v4)0.9f\n'%{"v1":hv_data[0][0][i], "v2":hv_data[0][2][i], "v3":hv_data[1][2][i] if i<13 else 0.0, "v4":hv_data[2][2][i] if i<11 else 0.0})

                if loopLength == 50:
                    for i in range(0, len(hv_data[0][0]), 1):
                        the_avg_file.write('%(v1)0.2f\t%(v2)0.9f\t%(v3)0.9f\t%(v4)0.9f\n'%{"v1":hv_data[0][0][i], "v2":hv_data[0][1][i], "v3":hv_data[1][1][i], "v4":hv_data[2][1][i]})
                        the_err_file.write('%(v1)0.2f\t%(v2)0.9f\t%(v3)0.9f\t%(v4)0.9f\n'%{"v1":hv_data[0][0][i], "v2":hv_data[0][2][i], "v3":hv_data[1][2][i], "v4":hv_data[2][2][i]})

                the_avg_file.close()
                the_err_file.close()

            PLOT_DATA = False
            if PLOT_DATA:
                # Make a plot of the comparison data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Loop Length / km'
                TheName = 'Linewidth'
                TheUnits = LWUNits
                args.y_label = TheName + TheUnits
                args.plt_range = [0, 165, 0, 3]
                args.fig_name = theLaser + '_' + TheName + '_D_' + '%(v1)d'%{"v1":loopLength}

                Plotting.plot_multiple_curves_with_errors(hv_data, args)

            del hv_data; del marks; del labels; 

            PLOT_COMBINE_DATA = True
            if PLOT_COMBINE_DATA:
                os.chdir(resDir)
                print(os.getcwd())
                # join the D = 10 data to the D = 50 data and make a plot of the linewidth
                # Read the D = 10 data
                D10data = numpy.loadtxt('Averaged_Data_D_10.txt', skiprows = 1, delimiter = '\t', unpack = True)
                D50data = numpy.loadtxt('Averaged_Data_D_50.txt', skiprows = 1, delimiter = '\t', unpack = True)
                data = numpy.concatenate((D10data, D50data), axis = 1) # concatenate the data sets
                
                # sorting according to distance data not strictly necessary, but nice to know it can be done
                data = data.T # transpose the data 
                data = data[data[:,0].argsort()] # sort according to the elements of the distance column
                data = data.T # undo the transpose
                
                D10data = numpy.loadtxt('Delta_Data_D_10.txt', skiprows = 1, delimiter = '\t', unpack = True)
                D50data = numpy.loadtxt('Delta_Data_D_50.txt', skiprows = 1, delimiter = '\t', unpack = True)
                deltadata = numpy.concatenate((D10data, D50data), axis = 1) # concatenate the data sets

                # sorting according to distance data not strictly necessary, but nice to know it can be done
                deltadata = deltadata.T # transpose the data 
                deltadata = deltadata[deltadata[:,0].argsort()] # sort according to the elements of the distance column
                deltadata = deltadata.T # undo the transpose
                
                # Make a plot of the combined data sets
                hv_data = []; labels = []; marks = []; 

                hv_data.append([data[0], data[1], deltadata[1]]); marks.append(Plotting.labs_pts[0]); labels.append('P$_{in}$ = %(v1)0.2f dBm'%{"v1":Pvals[0]})
                hv_data.append([data[0], data[2], deltadata[2]]); marks.append(Plotting.labs_pts[1]); labels.append('P$_{in}$ = %(v1)0.2f dBm'%{"v1":Pvals[1]})
                hv_data.append([data[0], data[3], deltadata[3]]); marks.append(Plotting.labs_pts[2]); labels.append('P$_{in}$ = %(v1)0.2f dBm'%{"v1":Pvals[2]})

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Loop Length / km'
                TheName = 'Linewidth'
                TheUnits = LWUNits
                args.y_label = TheName + TheUnits
                args.plt_range = [0, 760, 0.1, 2.7]
                args.fig_name = theLaser + '_' + TheName + '_Combined'

                Plotting.plot_multiple_curves_with_errors(hv_data, args)
                #Plotting.plot_multiple_curves(hv_data, args)

                SUBSET_LIN_FIT = False
                
                if SUBSET_LIN_FIT:
                    # Perform a linear fit to a subset of the beat data
                    D50data = numpy.loadtxt('Averaged_Data_D_50.txt', skiprows = 1, delimiter = '\t', unpack = True)
                    n_dist = len(D50data[0])
                    n_back = 13 # no. of data points to examine
                    hv_sub = []
                    #print(n_dist)
                    #print(data[0])
                    #print(data[0][n_dist - n_back:n_dist-1])
                
                    # hv_sub.append([data[0][n_dist - n_back:n_dist], data[1][n_dist - n_back:n_dist], deltadata[1][n_dist - n_back:n_dist] ]);
                    # hv_sub.append([data[0][n_dist - n_back:n_dist], data[2][n_dist - n_back:n_dist], deltadata[2][n_dist - n_back:n_dist] ]);
                    # hv_sub.append([data[0][n_dist - n_back:n_dist], data[3][n_dist - n_back:n_dist], deltadata[3][n_dist - n_back:n_dist] ]);
                
                    hv_sub.append([D50data[0][n_dist - n_back:n_dist], D50data[1][n_dist - n_back:n_dist] ]);
                    hv_sub.append([D50data[0][n_dist - n_back:n_dist], D50data[2][n_dist - n_back:n_dist] ]);
                    hv_sub.append([D50data[0][n_dist - n_back:n_dist], D50data[3][n_dist - n_back:n_dist] ]);

                    args.fig_name = theLaser + '_' + TheName + '_Combined_lin_fit'
                    Plotting.plot_multiple_linear_fit_curves(hv_sub, args)

                    # What are the slopes associated with the fits? 
                    # for i in range(0, len(hv_sub), 1):
                    #     Common.linear_fit(hv_sub[i][0], hv_sub[i][1], [1, 1], True)

                    # What are the averages associated with the fits? 
                    # for i in range(0, len(hv_sub), 1):
                    #     print(numpy.mean(hv_sub[i][1]),",",numpy.std(hv_sub[i][1]), ddof = 1)

                    del hv_sub

                del D10data; del D50data; del data; del deltadata; del hv_data; del marks; del labels;

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Extract_Data_From_Beat_File(beatfile, loud = False):

    # Extract the data from a single beat measurement file
    # data is stored in the beat file in columns of the form
    # 0: Beat No.   1: Fbeat / MHz  2: Distance / km    3: Time/ s  4: Tair/C   5: Taom/C   6: Taomdrv/C    7: Pmax/dBm 8: Fmax	
    # 9: LLest	10: LL_Vfit	11: LL_Lfit	12: LLest_-20	13: Voigt_h/nW	14: Voigt_c	15: Voigt_Lor_HWHM	16: Voigt_Gau_Stdev	17: Lor_h/nW	
    # 18: Lor_c 19: Lor_HWHM 20: P1/dBm	21: P2/dBm	22: P2/P1
    # return a list with data stored as elements of the list as follows
    # 0: Tair/C 1: Taom/C 2: Taomdrv/C 3: Pmax/dBm 4: Fmax 5: LLest	6: LL_Vfit	7: LL_Lfit	8: LLest_-20	
    # 9: Voigt_h/nW	10: Voigt_Lor_HWHM	11: Voigt_Gau_Stdev	12: Lor_h/nW 13: Lor_HWHM 14: P1/dBm 15: P2/dBm	16: P2/P1
    # R. Sheehan 13 - 12 - 2022

    FUNC_NAME = ".Extract_Data_From_Beat_File()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(beatfile):
            # read the data from the file
            df = pandas.read_csv(beatfile, delimiter = '\t')
            titles = list(df)
            Nbeats = df.shape[0]

            # Generate an array of indices of axes that you're interested in analysing
            dfaxes = numpy.arange(4, 23, 1)
            dfaxes = numpy.delete(dfaxes, [numpy.argwhere(dfaxes == 14), numpy.argwhere(dfaxes == 18)]) # not interested in Voigt fc (axis 14) or Lorentz fc (axis 18)

            # Extract the values from the data-frame and store them in an array
            data = [] # empty list for storing the data from the file
            sub_titles = [] # obtain the list of axes being analysed

            if loud:
                print('Extracting data from ',beatfile, ':', Nbeats,' beats measured')

            for i in range(0, len(dfaxes), 1):
                data.append( df[ titles[ dfaxes[i] ] ].to_numpy() )
                sub_titles.append(titles[ dfaxes[i] ])

            return [Nbeats, sub_titles, data]
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCould not find file: ' + beatfile + '\n'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Average_Data_From_Beat_Files(beatfiles):

    # this is now deprecated
    # use Aggregate_Data_From_Beat_Files instead
    # There's nothing wrong with it, but the alternate method is more pythonic and flexible
    # R. Sheehan 8 - 2 - 2024

    # look into multiple beat files
    # extract the data from each file
    # average the data obtained from each file
    # return the data as single array
    # R. Sheehan 13 - 12 - 2022

    # Extract_Data_From_Beat_File returns a list with data stored as elements of the list as follows
    # 0: Tair/C 1: Taom/C 2: Taomdrv/C 3: Pmax/dBm 4: Fmax 5: LLest	6: LL_Vfit	7: LL_Lfit	8: LLest_-20	
    # 9: Voigt_h/nW	10: Voigt_Lor_HWHM	11: Voigt_Gau_Stdev	12: Lor_h/nW 13: Lor_HWHM 14: P1/dBm 15: P2/dBm	16: P2/P1

    # ave_data holds the averaged value of each quantity from each beatfile
    # stdev_data holds the std. deviation value of each quantity from each beatfile
    # max_data holds the averaged value of each quantity from each beatfile
    # min_data holds the averaged value of each quantity from each beatfile

    # Some notes on copy
    # https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment

    FUNC_NAME = ".Average_Data_From_Beat_Files()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        ATTEMPTING_TO_USE = True
        if ATTEMPTING_TO_USE:
            ERR_STATEMENT = ERR_STATEMENT + '\nDO NOT USE!!!\nThis version of the code has been deprecated\n'
            raise Exception
        elif beatfiles is not None:
            # sum the data from each file
            ave_data = []; max_data = []; min_data = []; stdev_data = []; stdev_tmp = []; 

            sub_titles = []; Nbeats_max = -1000; Nfiles = len(beatfiles); 

            # loop over all the files
            # compute the average by summing the data from each beatfile and then dividing by no. files at the end
            # search each beatfile for the max value of each quantity over all beat files
            # search each beatfile for the min value of each quantity over all beat files
            # outer loop i counts into no. beatfiles, no. beat measurements that were made
            # inner loop j counts into no. beat notes in each beat file
            # average is computed over each of the j beat notes
            for i in range(0, Nfiles, 1):

                Nbeats, sub_titles, data = Extract_Data_From_Beat_File(beatfiles[i], False)         
                
                if Nbeats > Nbeats_max: Nbeats_max = Nbeats

                if i == 0:
                    # must use the copy method otherwise python assumes all the arrays are the same
                    # without copy, any manipulations performed on one list is performed on them all
                    ave_data = copy.deepcopy(data); 
                    max_data = copy.deepcopy(data); 
                    min_data = copy.deepcopy(data); 
                else:
                    # add the data from subsequent files to the data from the first file
                    # must account for the fact that different numbers of beats might be measured in each file
                    for j in range(0, len(ave_data), 1):

                        # Correct the lengths of the arrays holding the data
                        size_diff = len(ave_data[j]) - len(data[j])                  
                        
                        if size_diff > 0:
                            data[j] = numpy.append(data[j], numpy.zeros( size_diff ) )
                        elif size_diff < 0:
                            ave_data[j] = numpy.append(ave_data[j], numpy.zeros( abs(size_diff) ) )
                            max_data[j] = numpy.append(max_data[j], numpy.repeat( -1000, abs(size_diff)  ) )
                            min_data[j] = numpy.append(min_data[j], numpy.repeat( +1000, abs(size_diff)  ) )
                        else:
                            pass

                        # determine the max/min values
                        for k in range(0, len(data[j]), 1):
                            if data[j][k] > max_data[j][k]: max_data[j][k] = data[j][k]
                            if data[j][k] < min_data[j][k]: min_data[j][k] = data[j][k]

                        # compute the average sum
                        ave_data[j] = ave_data[j] + data[j]

            # Average the data obtained from all the files
            # Divde the sum over all the data by the number of Files
            Nfiles = float(Nfiles)
            for k in range(0, len(ave_data), 1):
                ave_data[k] = ave_data[k] / Nfiles
            
            del data; 

            return [Nbeats_max, sub_titles, ave_data, max_data, min_data] 
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nList beatfiles is None '
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Aggregate_Data_From_Beat_Files(beatfiles, loud = False):

    # Aggregate the data from multiple beatfiles
    # Use more sophisticated dataframe methods for computing the mean and std. dev. of the data in the beat files
    # See here for notes
    # https://stackoverflow.com/questions/67583994/mean-and-standard-deviation-with-multiple-dataframes
    # https://stackoverflow.com/questions/29438585/element-wise-average-and-standard-deviation-across-multiple-dataframes
    # See General.Data_Frame_Aggregation() for implementation

    # look into multiple beat files
    # extract the data from each file
    # average the data obtained from each file
    # determine the variation of each measurement, variation measured by std. dev. 
    # return the data as single array

    # data is stored in the beat file in columns of the form
    # 0: Beat No.   1: Fbeat / MHz  2: Distance / km    3: Time/ s  4: Tair/C   5: Taom/C   6: Taomdrv/C    7: Pmax/dBm 8: Fmax	
    # 9: LLest	10: LL_Vfit	11: LL_Lfit	12: LLest_-20	13: Voigt_h/nW	14: Voigt_c	15: Voigt_Lor_HWHM	16: Voigt_Gau_Stdev	17: Lor_h/nW	
    # 18: Lor_c 19: Lor_HWHM 20: P1/dBm	21: P2/dBm	22: P2/P1

    # Data is returned as a numpy array with the measured quantities stored as rows of the array as follows
    # 0: Beat No.   1: Fbeat / MHz  2: Distance / km    3: Time/ s  4: Tair/C   5: Taom/C   6: Taomdrv/C    7: Pmax/dBm 8: Fmax	
    # 9: LLest	10: LL_Vfit	11: LL_Lfit	12: LLest_-20	13: Voigt_h/nW	14: Voigt_Lor_HWHM	15: Voigt_Gau_Stdev	16: Lor_h/nW	
    # 17: Lor_HWHM 18: P1/dBm	19: P2/dBm	20: P2/P1

    # ave_data holds the averaged value of each quantity from each beatfile
    # dela_data holds the std. deviation value of each quantity from each beatfile
    
    # it would be easy to add the following should they be required
    # max_data holds the max value of each quantity from each beatfile
    # min_data holds the min value of each quantity from each beatfile

    # Some notes on copy
    # https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment

    # R. Sheehan 6 - 2 - 2024       

    FUNC_NAME = ".Aggregate_Data_From_Beat_Files()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if beatfiles is not None:

            # I've changed my mind on this, keeping the fbeat, time, distance data will allow
            # for comparison with longer loop length
            # Generate an array of indices of axes that you're interested in analysing
            # Don't need to worry about Beat No., Fbeat, Distance, Time
            dfaxes = numpy.arange(0, 23, 1)
            dfaxes = numpy.delete(dfaxes, [numpy.argwhere(dfaxes == 14), numpy.argwhere(dfaxes == 18)]) # not interested in Voigt fc (axis 14) or Lorentz fc (axis 18)

            # gather some statistics
            Nfiles = len(beatfiles); 
            Nbeats_max = -1000
            Nbeats_min = +1000
            the_df = []
            titles = []
            sub_titles = []

            # loop over all the files and read the data into memory
            for i in range(0, Nfiles, 1):
                if glob.glob(beatfiles[i]):
                    # to correctly concatenate the df assign a label to each one
                    # id column identifies the source of the dataframe
                    df = pandas.read_csv(beatfiles[i], delimiter = '\t').assign( id = 'Mset%(v1)d'%{"v1":i} )
                    titles = list(df)
                    Nbeats = df.shape[0]
                    if Nbeats > Nbeats_max: Nbeats_max = Nbeats
                    if Nbeats < Nbeats_min: Nbeats_min = Nbeats
                    the_df.append( df )

            # generate the list of sub-titles
            for i in range(0, len(dfaxes), 1):
                sub_titles.append( titles[ dfaxes[i] ] )

            # Concatenate the existing df into a single df
            # Now you have Nfiles Nrows*Ncols df combined into a single Nrows*Ncols dataframe
            # id column identifies the source of the dataframe so you haven't lost anything
            # can use id to access individual df
            nn_agg_df = len(the_df) # count no. aggregated df
            agg_df = pandas.concat( the_df )

            del the_df # no need to keep this data in memory

            if loud:
                print('\nDataFrame Titles, size = ',len(titles))
                print(titles)
                print('DataFrame sub-titles, size = ',len(sub_titles))
                print(sub_titles)
                print('dfaxes, size = ',len(dfaxes))
                print(dfaxes)
                print('No. concatenated df: ',nn_agg_df)
                print('Max. no. measured beats: ',Nbeats_max)
                print('Min. no. measured beats: ',Nbeats_min)
                print('\nConcatenated DataFrame')
                print(agg_df)
                print('\nSelect Individual DataFrame')
                print(agg_df[agg_df['id']=='Mset3'])

            # Make arrays to store the data
            # You want the measured quantities stored as rows of the array
            # why not make a data frame of the averaged quantities? 
            # You're making an array anyway, it's just one extra step to make it a dataframe
            # When you're making the plots you need direct access to the computed data which is easier to obtain using arrays
            # Store each measured quantity as a row of the array
            # Array size N_meas_quant rows * Nbeats_min cols
            # R. Sheehan 7 - 2 - 2024
            avg_data = numpy.zeros( ( len(sub_titles), Nbeats_min) ) # array for storing the averages
            delta_data = numpy.zeros( ( len(sub_titles), Nbeats_min) ) # array for storing the meas. errors
            
            # Loop over the concatenated df to extract the average and standard deviation values
            # See General.Data_Frame_Aggregation() for implementation
            for i in range(0, len(dfaxes), 1):
                for j in range(0, Nbeats_min, 1):
                    avg_data[i , j] = agg_df[ titles[ dfaxes[ i ] ] ][ j ].mean() # compute the average over each of the measurements at position j
                    delta_data[i , j] =  agg_df[ titles[ dfaxes[ i ] ] ][ j ].std() # compute the std. dev. over each of the measurements at position j

            return [Nbeats_min, sub_titles, avg_data, delta_data]
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nList beatfiles is None'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Beat_Data_Combo(Nbeats, F_AOM, Loop_Length, F_Start, F_CUTOFF, Titles, Choices, TheName, TheUnits, Average, Delta, loud = False):
    # plot combinations of the averaged data with error bars
    # Nbeats is the no. beat measurements that were made
    # F_AOM is the AOM phase shift frequency
    # Loop_Length is the length of the fibre loop in the LCR-DSHI
    # F_Start is beat frequency at which to start plotting, it can happen that the f_{b} = 80MHz signal may be bad so best to ignore it
    # F_CUTOFF is beat frequency at which to stop plotting, it usually happens that higher order beat frequencies do not produce good data
    # Titles is the list of names of the quantities that have been measured
    # Choices is an array of indices telling you what measured quantities to plot
    # TheName is a string that gives the figure name
    # TheUnits is a string that gives the units to be plotted along the y-axis
    # Average is the numpy array containing the averaged data from the beat measurements
    # Delta is the numpy array containing the std. dev. of the averaged data from the beat measurements
    # R. Sheehan 3 - 7 - 2023

    FUNC_NAME = ".Plot_Beat_Data_Combo()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        fbeats = numpy.arange(F_AOM, Nbeats*F_AOM + 1, F_AOM)
        distance = numpy.arange(Loop_Length, Nbeats*Loop_Length + 1, Loop_Length )
        fend_indx = 1 + numpy.where(fbeats == F_CUTOFF)[0][0]
        fstart_indx = int( -1 + ( F_Start / F_AOM ) )
        
        c1 = True if Nbeats > 0 else False
        c2 = True if len(Average) > 0 else False
        c3 = True if fstart_indx < fend_indx else False
        c4 = True if len(Choices) > 1 else False
        c10 = c1 and c2 and c3 and c4
        # must add more conditions here

        if c10:
            
            # Plot data measured between F_Start and F_CUTOFF Only
            PLOT_WITH_BEATS = False # Makes more sense to plot against distance rather than Beat Frequency

            xvals = fbeats if PLOT_WITH_BEATS else distance
            xlabel = 'Beat Frequency / MHz' if PLOT_WITH_BEATS else 'Loop Length / km'

            hv_data = []; labels = []; marks = []

            count = 0
            for i in Choices:
                avg_val = numpy.mean(Average[i][fstart_indx:fend_indx])
                avg_error = numpy.mean(Delta[i][fstart_indx:fend_indx])

                hv_data.append([xvals[fstart_indx:fend_indx], Average[i][fstart_indx:fend_indx], Delta[i][fstart_indx:fend_indx]]); 
                labels.append(Titles[i])
                marks.append(Plotting.labs_pts[count])
                
                count = count + 1

            args = Plotting.plot_arg_multiple()                

            args.loud = loud
            args.x_label = xlabel
            args.y_label = TheName + TheUnits
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.fig_name = TheName + '_Err'
                
            Plotting.plot_multiple_curves_with_errors(hv_data, args)

            del hv_data
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nError with input values'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Beat_Data(Nbeats, F_AOM, Loop_Length, F_Start, F_CUTOFF, Titles, Average, Delta, loud = False):

    # plot the averaged data with error bars
    # Nbeats is the no. beat measurements that were made
    # F_AOM is the AOM phase shift frequency
    # Loop_Length is the length of the fibre loop in the LCR-DSHI
    # F_Start is beat frequency at which to start plotting, it can happen that the f_{b} = 80MHz signal may be bad so best to ignore it
    # F_CUTOFF is beat frequency at which to stop plotting, it usually happens that higher order beat frequencies do not produce good data
    # Titles is the list of names of the quantities that have been measured
    # Average is the numpy array containing the averaged data from the beat measurements
    # Delta is the numpy array containing the std. dev. of the averaged data from the beat measurements
    # R. Sheehan 13 - 12 - 2022

    FUNC_NAME = ".Plot_Beat_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        fbeats = numpy.arange(F_AOM, Nbeats*F_AOM + 1, F_AOM)
        distance = numpy.arange(Loop_Length, Nbeats*Loop_Length + 1, Loop_Length )
        fend_indx = numpy.where(fbeats == F_CUTOFF)[0][0]
        fstart_indx = int( -1 + ( F_Start / F_AOM ) )
        
        c1 = True if Nbeats > 0 else False
        c2 = True if len(Average) > 0 else False
        c3 = True if fstart_indx < fend_indx else False
        c10 = c1 and c2 and c3
        # must add more conditions here

        if c10:
            
            PLOT_WITH_BEATS = False # Makes more sense to plot against distance rather than Beat Frequency

            xvals = fbeats if PLOT_WITH_BEATS else distance
            xlabel = 'Beat Frequency / MHz' if PLOT_WITH_BEATS else 'Loop Length / km'

            for i in range(4, len(Average), 1):
                avg_val = numpy.mean(Average[i][fstart_indx:fend_indx])
                avg_error = numpy.mean(Delta[i][fstart_indx:fend_indx])

                args = Plotting.plot_arg_single()                

                args.loud = loud
                args.x_label = xlabel
                args.y_label = Titles[i]
                args.fig_name = Titles[i].replace('/','_') + '_Err'
                args.plt_title = "Avg = %(v1)0.3f +/- %(v2)0.3f"%{"v1":avg_val, "v2":avg_error}
                
                Plotting.plot_single_linear_fit_curve_with_errors(xvals[fstart_indx:fend_indx], Average[i][fstart_indx:fend_indx], Delta[i][fstart_indx:fend_indx], args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nError with input values'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Beat_Data_Report(Nbeats, F_AOM, Loop_Length, F_Start, F_CUTOFF, Titles, Average, Delta, res_filename):

    # Print a report on the averaged beat data values
    # R. Sheehan 15 - 12 - 2022

    FUNC_NAME = ".Beat_Data_Report()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:

        fbeats = numpy.arange(F_AOM, Nbeats*F_AOM + 1, F_AOM)
        fstart_indx = int( -1 + ( F_Start / F_AOM ) )
        fend_indx = 1 + numpy.where(fbeats == F_CUTOFF)[0][0]

        c1 = True if Nbeats > 0 else False
        c2 = True if len(Average) > 0 else False
        c3 = True if fstart_indx < fend_indx else False
        c10 = c1 and c2 and c3
        # must add more conditions here, I think
        # R. Sheehan 8 - 2 - 2024

        if c10:
            # Redirect the output to a file
            old_target, sys.stdout = sys.stdout, open(res_filename, 'w')

            print("System Settings")
            print("Loop length:",Loop_Length,"km")
            print("f_{AOM}:",F_AOM,"MHz")
            print("Nbeats Sampled:",Nbeats)
            print("Nbeats Useful:",fend_indx - fstart_indx)
            print("f_{cuttoff}:",F_CUTOFF,"MHz")
            print("Effective Loop Length:",fend_indx*Loop_Length,"km")            

            print("\nResults")
            print("Quantitites reported here are averaged over all the beat measurements")
            print("e.g. Tair/C = Average(Tair_beat_1 + Tair_beat_2 + ... Tair_beat_n) +/- Average(deltaTair_beat_1 + deltaTair_beat_2 + ... deltaTair_beat_n)\n")
            for i in range(0, len(Average), 1):
                avg_val = numpy.mean(Average[i][fstart_indx:fend_indx])
                avg_delta = numpy.mean(Delta[i][fstart_indx:fend_indx])      
                print("%(v1)s: %(v2)0.3f +/- %(v3)0.3f"%{"v1":Titles[i], "v2":avg_val, "v3":avg_delta})

            sys.stdout = old_target # return to the usual stdout
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nError with input values'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def NKT_LCR_DSHI_Test():

    # plot the data obtained while optimising the LCR-DSHI setup
    # for testing the NKT Fibre Laser
    # R. Sheehan 23 - 2 - 2023

    FUNC_NAME = ".NKT_LCR_DSHI_Test()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/NKT_LCR_DSHI/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Plot the measured NKT OPtical Spectrum
            PLOT_OPT_SPCTR = False
            if PLOT_OPT_SPCTR:
                opt_spctr = glob.glob('NKT_Laser_I_*.txt')
                Ipump = [100, 125, 150]

                hv_data = []; labels = []; marks = []; 

                for i in range(0, len(opt_spctr), 1):
                    data = numpy.loadtxt(opt_spctr[i], delimiter = '\t',unpack = True)
                    hv_data.append(data);
                    marks.append(Plotting.labs_lins[i])
                    labels.append('I$_{pump}$ = %(v1)d (mA)'%{"v1":Ipump[i]})

                # Make the plot
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Wavelength ( nm )'
                args.y_label = 'Power ( dBm / 0.05 nm )'
                args.plt_range = [1549, 1551, -50, 10]
                args.fig_name = 'NKT_Optical_Spectrum'

                Plotting.plot_multiple_curves(hv_data, args)

            # Plot the Measured CNR
            PLOT_CNR = False
            if PLOT_CNR:
                NKT_CNR = 'NKT_I_100_CNR.txt'
                data = numpy.loadtxt(NKT_CNR, delimiter = '\t', unpack = True)

                args = Plotting.plot_arg_single()
                
                args.loud = True
                args.x_label = 'VOA Bias ( V )'
                args.y_label = 'CNR ( dB )'
                args.fig_name = 'NKT_CNR'
                args.plt_range = [0, 4, 26, 44]
                
                Plotting.plot_single_curve_with_errors(data[0], data[1], data[2], args)

            # Plot lineshape RBW = 20 kHz
            PLOT_LINE_20 = False
            if PLOT_LINE_20:
                line_20_files = glob.glob('NKT_I_100_Vb_*_RBW_20_fb_80.txt')
                VOA_bias = [0, 1, 2, 3, 3.5, 4, 4.5]

                hv_data = []; labels = []; marks = []; 

                for i in range(0, len(line_20_files), 1):
                    data = numpy.loadtxt(line_20_files[i], delimiter = '\t',unpack = True)
                    hv_data.append(data);
                    marks.append(Plotting.labs_lins[i])
                    labels.append('V$_{VOA}$ = %(v1)0.1f V'%{"v1":VOA_bias[i]})

                # Make the plot
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm / 20 kHz )'
                args.plt_range = [79, 81, -100, -10]
                args.fig_name = 'NKT_Lineshape_RBW_20'

                Plotting.plot_multiple_curves(hv_data, args)

            # Plot lineshape Variable RBW
            PLOT_LINE_VaryR = False
            if PLOT_LINE_VaryR:
                line_vary_files = ['NKT_I_100_Vb_30_RBW_20_fb_80.txt', 'NKT_I_100_Vb_30_RBW_2_fb_80.txt', 'NKT_I_100_Vb_30_RBW_1_fb_80.txt','NKT_I_100_Vb_30_RBW_05_fb_80.txt']
                print(line_vary_files)
                RBW = [20, 2, 1, 0.5]

                hv_data = []; labels = []; marks = []; 

                for i in range(0, len(line_vary_files), 1):
                    data = numpy.loadtxt(line_vary_files[i], delimiter = '\t',unpack = True)
                    hv_data.append(data);
                    marks.append(Plotting.labs_lins[i])
                    labels.append('RBW = %(v1)0.1f kHz'%{"v1":RBW[i]})

                # Make the plot
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm )'
                args.plt_range = [79.75, 80.25, -90, -10]
                args.plt_title = 'V$_{VOA}$ = 3 V'
                args.fig_name = 'NKT_Lineshape_RBW_Variable'

                Plotting.plot_multiple_curves(hv_data, args)

            # Plot all beat notes
            PLOT_ALL_BEATS = False
            if PLOT_ALL_BEATS:
                fbeats = numpy.arange(80, 2970, 80)
                
                fcentre = deltaf = 80
                span = 0.25
                flo = fcentre - 0.5*span
                fhi = fcentre + 0.5*span
                Lf = 50

                # Store data for combined plot
                hv_data = []; labels = []; marks = []; dist_labels = []; 

                # Extract data showing the blue-shift of the frequency peak
                delta_peak = []

                for i in range(0, len(fbeats), 1):
                    beat_file = glob.glob('NKT_I_100_Vb_30_RBW_05_fb_%(v1)d.txt'%{"v1":fbeats[i]})

                    data = numpy.loadtxt(beat_file[0], delimiter = '\t', unpack = True)

                    # Extract data showing the blue-shift of the frequency peak
                    delta_peak.append( 1e+3*( data[0][numpy.argmax(data[1])] - fbeats[i] ) )

                    # Change the scale for the plot
                    data[0] = 1e+3*(data[0] - fbeats[i]) # shift all measured frequencies to 0 MHz

                    # Plot the measured spectrum
                    args = Plotting.plot_arg_single()

                    args.loud = False
                    args.marker = Plotting.labs_lins[ i % len(Plotting.labs_lins) ]
                    args.x_label = 'Frequency ( kHz )'
                    args.y_label = 'Spectral Power ( dBm / 500 Hz )'
                    args.plt_range = [-500*span, 500*span, -120, -20]
                    args.plt_title = 'V$_{VOA}$ = 3 V'
                    args.fig_name = beat_file[0].replace('.txt','')

                    Plotting.plot_single_curve(data[0], data[1], args)

                    # Store data for combined plot
                    
                    hv_data.append([ data[0], data[1] ] )
                    marks.append(Plotting.labs_lins[ i % len(Plotting.labs_lins) ])
                    labels.append('f$_{b}$ = %(v1)d MHz'%{"v1":fbeats[i]})
                    dist_labels.append('D = %(v1)d km'%{"v1":(i+1)*Lf})

                    flo = flo + deltaf
                    fhi = fhi + deltaf

                # Plot the deviation of the peak from the expected value
                args = Plotting.plot_arg_single()

                args.loud = True
                args.marker = Plotting.labs[2]
                args.x_label = 'Beat Frequency ( MHz )'
                args.y_label = 'Peak Deviation ( kHz )'
                #args.plt_range = [flo, fhi, -90, -10]
                args.fig_name = 'Peak_Freq_Deviation'

                Plotting.plot_single_linear_fit_curve(fbeats, delta_peak, args)

                # What is the linear fit?
                Common.linear_fit(fbeats, delta_peak, [-1, 1], True)

                # Plot all the beats in a single plot
                # Extract subset of data
                hv_sub = []; lab_sub = []; mark_sub = []
                for i in range(0, len(hv_data)-9, 4):
                    hv_sub.append(hv_data[i]); lab_sub.append(dist_labels[i]); mark_sub.append(marks[i]); 
                
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = lab_sub
                args.mrk_list = mark_sub
                args.x_label = 'Frequency ( kHz )'
                args.y_label = 'Spectral Power ( dBm / 500 Hz )'
                args.plt_range = [-500*span, 500*span, -110, -20]
                args.plt_title = 'V$_{VOA}$ = 3 V'
                args.fig_name = 'NKT_Lineshape_Combined_2'

                Plotting.plot_multiple_curves(hv_sub, args)

            # Plot Initial Estimates of Fitted LLM
            PLOT_INIT_FITTED = True
            if PLOT_INIT_FITTED:
                hv_data = []; labels = []; marks = []; 
                fit_res_1 = 'NKT_Fitting_Results_1.txt'
                data = numpy.loadtxt(fit_res_1, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]]); labels.append('Estimated / kHz'); marks.append(Plotting.labs[0]); 
                hv_data.append([data[0], data[2]]); labels.append('Voigt / kHz'); marks.append(Plotting.labs[1]); 
                hv_data.append([data[0], data[3]]); labels.append('Lorentz / kHz'); marks.append(Plotting.labs[2]); 

                nmeas = len(data[0])
                ndrop = 15

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Beat Frequency ( MHz )'
                args.y_label = 'Laser Linewidth (kHz)'
                args.plt_range = [0, 3000, 0, 6]
                args.plt_title = 'V$_{VOA}$ = 3 V'
                args.fig_name = 'NKT_Fitting_Results_1'

                Plotting.plot_multiple_curves(hv_data, args)

                # Compute the average 
                print('Estimated: ',numpy.mean(data[1][0:nmeas-ndrop]),' +/- ',0.5*( numpy.max(data[1][0:nmeas-ndrop]) - numpy.min(data[1][0:nmeas-ndrop]) ),' kHz')
                print('Estimated: ',numpy.mean(data[2][0:nmeas-ndrop]),' +/- ',0.5*( numpy.max(data[2][0:nmeas-ndrop]) - numpy.min(data[2][0:nmeas-ndrop]) ),' kHz')
                print('Estimated: ',numpy.mean(data[3][0:nmeas-ndrop]),' +/- ',0.5*( numpy.max(data[3][0:nmeas-ndrop]) - numpy.min(data[3][0:nmeas-ndrop]) ),' kHz')

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find directory: ' + DATA_HOME + '\n'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Multiple_Spectra_Old_Deprecated(DATA_HOME, RBW_Val = 500, Tmeas = 20, theXUnits = 'kHz', theYUnits = 'Hz', Deff = 400, Pin = 0, VVOA = 3.5):

    # DO NOT USE!!!!
    # Code Deprecated New Version Improved Version Available
    # R. Sheehan 24 - 1 - 2024

    # Generate a plot of all the measured spectra from a Multi-LLM measurement
    # DATA_HOME is the name of the directory in which the files 'LLM_Meas_*.txt' are stored
    # RBW_Val is the value of the resolution BW used to perform the measurement
    # Tmeas is the approximate time that was needed to perform the measurement
    # theXunits are the Frequency units that you want displayed along the x-axis
    # theYUnits are the Frequency units of the RBW value that you want displayed along the y-axis
    # Deff is the effective loop length used to perform the measurement, units of km
    # Pin is the output power from the laser / input power to the LCR-DSHI loop, units of dBm
    # VVOA is the VOA bias that was applied at the time of the measurement, unit of V
    # R. Sheehan 30 - 5 - 2023
    # Updated R. Sheehan 22 - 1 - 2024

    FUNC_NAME = ".Plot_Multiple_Spectra_Old_Deprecated()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_400/LLM_Data_Nmeas_200_I_100_29_05_2023_14_20_Span_500k/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_400/LLM_Data_Nmeas_200_I_200_31_05_2023_10_12/'
        
        ATTEMPTING_TO_USE = True
        if ATTEMPTING_TO_USE:
            ERR_STATEMENT = ERR_STATEMENT + '\nDO NOT USE!!!\nThis version of the code has been deprecated\n'
            raise Exception
        elif os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            files = glob.glob('LLM_Meas_*.txt')
            files.sort(key=lambda f: int(re.sub(r'\D', '', f))) # sort the filenames in place using the number within the string, assumes single digit in string

            hv_data = []; marks = []; labels = []; 
            deltaT = Tmeas / 60.0 # measurement time in mins
            xlow = 0.0; xhigh = 0.0; 
            #nskip = 8 # only plot every nskip measurements, NKT
            nskip = 5 # only plot every nskip measurements, CoBrite
            for i in range(0, len(files), nskip):
                values = Common.extract_values_from_string(files[i])
                theTime = float(values[0])*deltaT
                data = numpy.loadtxt(files[i], delimiter = '\t')
                if xlow == 0.0 and xhigh == 0.0:
                    xlow = data[0][0]; xhigh = data[0][-1];
                hv_data.append(data); marks.append(Plotting.labs_dotdash[i%len(Plotting.labs_dotdash)]); labels.append('T = %(v1)0.1f mins'%{"v1":theTime})

            # make a plot
            args = Plotting.plot_arg_multiple()

            args.loud = False
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency / %(v1)s'%{"v1":theXUnits}
            args.y_label = 'Power / dBm / %(v1)d%(v2)s'%{"v1":RBW_Val, "v2":theYUnits}
            args.plt_range = [xlow, xhigh, -90, -20]
            args.fig_name = 'Measured_Spectra'
            args.plt_title = 'D$_{eff}$ = %(v1)d km, P$_{in}$ = %(v2)0.1f dBm, V$_{VOA}$ = %(v3)0.1f V'%{"v1":Deff, "v2":Pin, "v3":VVOA}

            Plotting.plot_multiple_curves(hv_data, args)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_Multi_LLM_Analysis():

    # Perform the multi-llm analysis calculations for multiple sets of measurements
    # i.e. Analyse the Multi-LLM data as a function of voa bias / loop power ratio and Input Power
    # R. Sheehan 6 - 6 - 2023

    # Update 22 - 1 - 2024
    # Split the script in two, one part performs the multi-multi-llm analysis
    # another generates the plots for the power variation analysis
    # can you generalise this to look at measurements as a function of Fspan / RBW? 
    # Do you even want to? 

    FUNC_NAME = ".Multi_Multi_LLM_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # loop the Multi-LLM Analysis calculations over a list of directories
        # gather the averaged data as a function of VOA bias / loop power Ratio

        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_200/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_400/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_CoBriteTLS_T_25_D_400/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_JDSU_DFB_T_20_D_400/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Make a directory for storing the results
            resDir = 'Loop_Power_Variation_Mar_25/'
            #resDir = 'Loop_Power_Variation_FSpan_100/'
            #resDir = 'Loop_RBW_Variation/'
            #resDir = 'JDSU_I_Variation/'
            if not os.path.isdir(resDir): os.mkdir(resDir)

            # Generate the list of directories to be analysed
            
            # Parameters for the NKT measurement
            #Ival = 100; Day = '19';  
            #Ival = 200; Day = '20';
            #Ival = 300; Day = '21';
            #Month = '06';
            
            #Ival = 100; Day = '17';  
            #Ival = 200; Day = '18';
            #Ival = 300; Day = '19';
            #Month = '02';            
            #Nmeas = 200
            
            #Ival = 100; Day = '25';  
            #Ival = 200; Day = '26';
            #Ival = 300; Day = '27';
            #Month = '02';
            #Nmeas = 100

            #Ival = 100; Day = '03';  
            #Ival = 200; Day = '04';
            Ival = 300; Day = '05';
            Month = '03';
            Nmeas = 100
            
            # NKT parameters
            RBW = 100; theYunits = 'Hz' # RBW and its units for the NKT measurement
            Tmeas = 28.5; # Approximate measurement time in seconds for the NKT measurement
            Deff = 200 # Effective loop length in km
            theXunits = 'kHz' # Frequency units along X-axis
            
            # Parameters for the CoBrite measurement
            #Ival = 100; Day = '07';  
            #Ival = 200; Day = '10';
            #Ival = 300; Day = '10';
            #Month = '07'; 
            #Nmeas = 100
            ## CoBrite Parameters
            #RBW = 5; theYunits = 'kHz' # RBW and its units for the CoBrite measurement
            #Tmeas = 15; # Approximate measurement time in seconds for the CoBrite measurement
            #Deff = 400 # Effective loop length in km
            #theXunits = 'MHz' # Frequency units along X-axis
            
            # Parameters for the JDSU measurement
            #Ival = 50; Day = '22';  
            #Ival = 70; Day = '22';
            #Ival = 90; Day = '22';
            #Month = '02'; 
            #Nmeas = 200
            # CoBrite Parameters
            #RBW = 20; theYunits = 'kHz' # RBW and its units for the CoBrite measurement
            #Tmeas = 33.9; # Approximate measurement time in seconds for the CoBrite measurement
            #Deff = 400 # Effective loop length in km
            #theXunits = 'MHz' # Frequency units along X-axis
            
            dir_list = glob.glob('LLM_Data_Nmeas_%(v4)d_I_%(v1)d_%(v3)s_%(v2)s_*/'%{"v4":Nmeas, "v1":Ival, "v3":Day, "v2":Month})
            #dir_list = ['LLM_Data_Nmeas_200_I_100_05_07_2023_13_37/', 'LLM_Data_Nmeas_200_I_200_05_07_2023_11_00/', 'LLM_Data_Nmeas_200_I_300_05_07_2023_09_58/']
            #dir_list = ['LLM_Data_Nmeas_200_I_100_09_06_2023_09_42_Span_50k/', 'LLM_Data_Nmeas_200_I_100_08_06_2023_12_57_Span_100k/', 'LLM_Data_Nmeas_200_I_100_29_05_2023_15_34_Span_250k/', 'LLM_Data_Nmeas_200_I_100_29_05_2023_14_20_Span_500k/']
            #TmeasVals = [39, 29, 19, 20] # measurement time varies depending on the RBW value and the Freq. Span
            #dir_list = dir_list[2:len(dir_list)]

            # Obtain the loop power data from all the measurements
            PARSE_ESA_FILES = True
            LoopPowerFileName = 'Loop_Power_Values_I_%(v1)d.txt'%{"v1":Ival}

            # Create files for storing the accumulated data
            # Create a file for storing the loop power data values
            if os.path.isdir(resDir) and PARSE_ESA_FILES:
                os.chdir(resDir)
                if not glob.glob(LoopPowerFileName): 
                    esaFile = open(LoopPowerFileName,'x') # create the file to be written to
                    esaFile.write('VOA Bias ( V )\tInput Power (dBm)\tLoop Power (dBm)\tPower Ratio P2 / P1\tFspan (Hz)\tRBW (Hz)\n') # write the file header
                    esaFile.close()
                os.chdir(DATA_HOME)
            
            PERFORM_MULTI_LLM = True # Tells the code to run the Multi-LLM analysis on the data contained in the directory
            
            if len(dir_list) > 0:

                for i in range(0, len(dir_list), 1): 
                    # Extract the Power versus VOA data, store the results in LoopPowerFileName
                    theVals = Parse_ESA_Settings(dir_list[i])                        
                    VVOA = theVals['VVoa']
                    Pin = theVals['P1']
                    RBW = theVals['RBW']
                    print(theVals['VVoa'],' , ',theVals['P2/P1'], ',', theVals['FSpan'], ',', theVals['RBW'])
                    os.chdir(DATA_HOME)

                    if PARSE_ESA_FILES:                        
                        os.chdir(resDir)
                        esaFile = open(LoopPowerFileName,'a')
                        esaFile.write('%(v1)0.3f\t%(v2)0.3f\t%(v3)0.3f\t%(v4)0.3f\t%(v5)0.3f\t%(v6)0.3f\n'%{"v1":theVals['VVoa'], "v2":theVals['P1'], "v3":theVals['P2'], "v4":theVals['P2/P1'], "v5":theVals['FSpan'], "v6":theVals['RBW']})
                        esaFile.close()
                        os.chdir(DATA_HOME)
                    
                    # Do the Multi-LLM Analysis on each measured data
                    if PERFORM_MULTI_LLM:
                        Multi_LLM_Analysis(dir_list[i], RBW, Tmeas, theXunits, theYunits, Deff, Pin, VVOA)
                        os.chdir(DATA_HOME)
            else:
                ERR_STATEMENT = ERR_STATEMENT + '\ndir_list is empty'
                raise Exception
        else:
            raise Exception        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Summarise_Multi_LLM_Analysis():

    # Generate a summary of the data obtained from multiple Multi-LLM Measurements
    # R. Sheehan 22 - 1 - 2024

    FUNC_NAME = ".Summarise_Multi_LLM_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # loop the Multi-LLM directories gather the averaged data
        # In this case as a function of VOA bias / loop power Ratio

        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_200/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_400/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_CoBriteTLS_T_25_D_400/'
        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_JDSU_DFB_T_20_D_400/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Make a directory for storing the results
            #resDir = 'Loop_Power_Variation_Feb_25/'
            resDir = 'Loop_Power_Variation_Mar_25/'
            #resDir = 'Loop_Power_Variation_FSpan_100/'
            #resDir = 'Loop_RBW_Variation/'
            #resDir = 'JDSU_I_Variation/'
            if not os.path.isdir(resDir): os.mkdir(resDir)
            
            # Parameters for the NKT measurement
            # June 2023
            #Ival = 100; Day = '19';  Pin = 3.356; 
            #Ival = 200; Day = '20'; Pin = 9.313; 
            #Ival = 300; Day = '21'; Pin = 11.767; 
            #Month = '06'; 
            
            # Feb 2025
            #Ival = 100; Day = '17';  Pin = 3.7265; 
            #Ival = 200; Day = '18'; Pin = 9.452; 
            #Ival = 300; Day = '19'; Pin = 11.879; 
            #Month = '02'; 
            #Nmeas = 200; 
            
            # Mar 2025
            #Ival = 100; Day = '25';  Pin = 3.769; 
            #Ival = 200; Day = '26'; Pin = 9.519;
            #Ival = 300; Day = '27'; Pin = 11.934;
            #Month = '02'; 
            #Nmeas = 100;

            ## Input powers for the NKT data set
            #Pvals = [3.356, 9.313, 11.767]
            #Perr = [0.016, 0.015, 0.013]
            
            # Mar 2025
            #Ival = 100; Day = '03';  Pin = 3.769; 
            #Ival = 200; Day = '04'; Pin = 9.519;
            Ival = 300; Day = '05'; Pin = 11.934;
            Month = '03'; 
            Nmeas = 100;
            
            # Input powers for the NKT data set
            Pvals = [3.803, 9.507, 11.926]
            Perr = [0.059, 0.009, 0.001]
            
            RBWstr = '100Hz'; LLMunitstr = 'kHz'; Deff = 200; RBWValue = 100; 
            
            # Parameters for the CoBrite measurement
            #Ival = 100; Day = '07'; Pin = 4.365; 
            #Ival = 200; Day = '10'; Pin = 5.512; 
            #Ival = 300; Day = '10'; Pin = 6.539; 
            #Month = '07'; Nmeas = 100; 
            
            ## Input powers for the CoBrite data set
            #Pvals = [4.365, 5.512, 6.539]
            #Perr = [0.066, 0.011, 0.018]
            #RBWstr = '5kHz'; LLMunitstr = 'MHz'; Deff = 400;
            
            # Parameters for the JDSU measurement
            #Ival = 50; Day = '22'; Pin = 5.880; 
            #Ival = 70; Day = '22'; Pin = 7.741; 
            #Ival = 90; Day = '22'; Pin = 9.045; 
            #Month = '02'; Nmeas = 200; 
            # Input powers for the CoBrite data set
            #Pvals = [5.880, 7.741, 9.045]
            #Perr = [0.001, 0.001, 0.001]
            #RBWstr = '20kHz'; LLMunitstr = 'MHz'; Deff = 400; 
            
            dir_list = glob.glob('LLM_Data_Nmeas_%(v4)d_I_%(v1)d_%(v3)s_%(v2)s_*/'%{"v4":Nmeas, "v1":Ival, "v3":Day, "v2":Month})
            #dir_list = dir_list[2:len(dir_list)]
            #dir_list = ['LLM_Data_Nmeas_200_I_100_09_06_2023_09_42_Span_50k/', 'LLM_Data_Nmeas_200_I_100_08_06_2023_12_57_Span_100k/', 'LLM_Data_Nmeas_200_I_100_29_05_2023_15_34_Span_250k/', 'LLM_Data_Nmeas_200_I_100_29_05_2023_14_20_Span_500k/']
            #TmeasVals = [39, 29, 19, 20] # measurement time varies depending on the RBW value and the Freq. Span
            #SpanVals = [50, 100, 250, 500]
            #RBWVals = [50, 100, 500, 500]
            #RBWVals = [20]
            #Pin = 3.34
            
            PARSE_RES_FILES = False # Must be false until all Multi-LLM results are obtained
            esaResFileName = 'Measurement_Results_I_%(v1)d.txt'%{"v1":Ival}
            esaErrFileName = 'Measurement_Errors_I_%(v1)d.txt'%{"v1":Ival}

            # Make a plot of the fitted lineshape spectra versus for each Pin value
            PLOT_FITTED_SPECTRA = False

            # Create files for storing the accumulated data from multuple Multi-LLM runs
            # Output is of the form ['Pmax/dBm', 'LLest', 'LL_Vfit', 'LL_Lfit', 'LLest_-20', 'Voigt_Lor_HWHM', 'Voigt_Gau_Stdev', 'P1/dBm', 'P2/dBm', 'P2/P1']
            if os.path.isdir(resDir) and PARSE_RES_FILES:
                os.chdir(resDir)
                if not glob.glob(esaResFileName): 
                    esaFile = open(esaResFileName,'x') # create the file to be written to
                    esaFile.write('Input Power (dBm)\tLoop Power (dBm)\tPower Ratio P2 / P1\tPmax (dBm)\tLLest\tLL_Vfit\tLL_Lfit\tLLest_-20\tVoigt_Lor_HWHM\tVoigt_Gau_Stdev\tRBW\n') # write the file header
                    esaFile.close()
                if not glob.glob(esaErrFileName): 
                    esaFile = open(esaErrFileName,'x') # create the file to be written to
                    esaFile.write('Input Power (dBm)\tLoop Power (dBm)\tPower Ratio P2 / P1\tPmax (dBm)\tLLest\tLL_Vfit\tLL_Lfit\tLLest_-20\tVoigt_Lor_HWHM\tVoigt_Gau_Stdev\tRBW\n') # write the file header
                    esaFile.close()
                os.chdir(DATA_HOME)

            if len(dir_list) > 0:
                if PARSE_RES_FILES:
                    for i in range(0, len(dir_list), 1): 
                        # Extract the Measurement Results
                        # Output is of the form ['Pmax/dBm', 'LLest', 'LL_Vfit', 'LL_Lfit', 'LLest_-20', 'Voigt_Lor_HWHM', 'Voigt_Gau_Stdev', 'P1/dBm', 'P2/dBm', 'P2/P1']
                        # This can only run once Multi-LLm is complete
                        theVals, theErrs = Parse_Results_Summary(dir_list[i])
                        #print(theVals['VVoa'],' , ',theVals['P2/P1'] )
                        os.chdir(DATA_HOME)
                        os.chdir(resDir)

                        esaFile = open(esaResFileName,'a')
                        esaFile.write('%(v1)0.5f\t%(v2)0.5f\t%(v3)0.5f\t%(v4)0.5f\t%(v5)0.5f\t%(v6)0.5f\t%(v7)0.5f\t%(v8)0.5f\t%(v9)0.5f\t%(v10)0.5f\t%(v11)0.1f\n'%{"v1":theVals['P1/dBm'], "v2":theVals['P2/dBm'], "v3":theVals['P2/P1'], "v4":theVals['Pmax/dBm'], 
                                                                                                                                                            "v5":theVals['LLest'], "v6":theVals['LL_Vfit'], "v7":theVals['LL_Lfit'], "v8":theVals['LLest_-20'], 
                                                                                                                                                            "v9":theVals['Voigt_Lor_HWHM'], "v10":theVals['Voigt_Gau_Stdev'], "v11":RBWValue } )
                        esaFile.close()

                        esaFile = open(esaErrFileName,'a')
                        esaFile.write('%(v1)0.5f\t%(v2)0.5f\t%(v3)0.5f\t%(v4)0.5f\t%(v5)0.5f\t%(v6)0.5f\t%(v7)0.5f\t%(v8)0.5f\t%(v9)0.5f\t%(v10)0.5f\t%(v11)0.1f\n'%{"v1":theErrs['P1/dBm'], "v2":theErrs['P2/dBm'], "v3":theErrs['P2/P1'], "v4":theErrs['Pmax/dBm'], 
                                                                                                                                                            "v5":theErrs['LLest'], "v6":theErrs['LL_Vfit'], "v7":theErrs['LL_Lfit'], "v8":theErrs['LLest_-20'], 
                                                                                                                                                            "v9":theErrs['Voigt_Lor_HWHM'], "v10":theErrs['Voigt_Gau_Stdev'], "v11":RBWValue } )
                        esaFile.close()
                        os.chdir(DATA_HOME)

                if PLOT_FITTED_SPECTRA:
                    # Make a plot of the fitted lineshape spectra versus for each Pin value

                    PLOT_IN_DBM = True # Always plot in DBM since the measured data is output in units of dBm

                    # Gather the data for each Pin
                    #VVOA = numpy.arange(2.8, 4.0, 0.2)
                    #VVOA = numpy.arange(0, 2.6, 0.5)
                    VVOA = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
                    xlow = 0.0; xhigh = 0.0; # variables for storing the enpoints of the frequency plot range
                    hv_data = []; marks = []; labels = []; 
                    count_mrk = 0
                    for i in range(0, len(dir_list), 1):
                        os.chdir(dir_list[i])
                        data = numpy.loadtxt("Voigt_Average.txt", delimiter = ',', unpack = True)
                        if xlow == 0.0 and xhigh == 0.0:
                            xlow = data[0][0]; xhigh = data[0][-1];
                        if PLOT_IN_DBM:
                            data[1] = data[1] / 1e+6 # convert uW -> mW
                            data[1] = Common.list_convert_mW_dBm(data[1]) # convert mW -> dBm
                        hv_data.append(data); marks.append(Plotting.labs_lins[count_mrk%len(Plotting.labs_lins)]); 
                        labels.append('V$_{VOA}$ = %(v1)0.1f V'%{"v1":VVOA[i]})
                        #labels.append('RBW/Spn=%(v2)dHz/%(v1)dkHz'%{"v1":SpanVals[i], "v2":RBWVals[i]})
                        count_mrk = count_mrk + 1
                        os.chdir(DATA_HOME)

                    # Make the plot
                    os.chdir(resDir)
                    args = Plotting.plot_arg_multiple()

                    args.loud = True
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'Frequency / %(v1)s'%{"v1":LLMunitstr}
                    args.y_label = 'Spectral Power / dBm / %(v1)s'%{"v1":RBWstr}
                    #args.y_label = 'Spectral Power / dBm'
                    args.fig_name = 'Fitted_Voigt_Lineshapes_I_%(v1)d'%{"v1":Ival}
                    args.plt_title = 'D$_{eff}$ = %(v1)d km, P$_{in}$ = %(v2)0.2f dBm'%{"v1":Deff, "v2":Pin}
                    #args.plt_range = [xlow, xhigh, -90, -20]
                    #args.plt_range = [-100, 100, -80, -30]
                    #args.plt_range = [-50, 50, -70, -25]

                    Plotting.plot_multiple_curves(hv_data, args)

                    del hv_data; del marks; del labels; 
                    os.chdir(DATA_HOME)
            else:
                ERR_STATEMENT = ERR_STATEMENT + '\ndir_list is empty'
                raise Exception

            # Make a plot of the loop power value data as function of VVOA
            PLOT_LOOP_POWER_VALUES = False

            if PLOT_LOOP_POWER_VALUES:
                os.chdir(resDir)
                hv_data1 = []; labels1 = []; marks1 = []
                hv_data2 = []; labels2 = []; marks2 = []
                Ivals = [100, 200, 300]
                #RBWVals = [50, 100, 250, 500]
                
                # Input powers for the NKT data set, June 2023
                #Pvals = [3.356, 9.313, 11.767]
                #Perr = [0.016, 0.015, 0.013]
                
                # Input powers for the NKT data set, February 2025
                #Pvals = [3.7265, 9.452, 11.879]
                #Perr = [0.015, 0.036, 0.025]
                
                # Input powers for the NKT data set, March 2025
                Pvals = [3.769, 9.519, 11.934]
                Perr = [0.016, 0.013, 0.025]

                # Input powers for the CoBrite data set
                #Pvals = [4.365, 5.512, 6.539]
                #Perr = [0.066, 0.011, 0.018]

                for i in range(0, len(Ivals), 1):
                    LoopPowerFileName = 'Loop_Power_Values_I_%(v1)d.txt'%{"v1":Ivals[i]}
                    data = numpy.loadtxt(LoopPowerFileName, delimiter = '\t', unpack = True, skiprows = 1)
                    print('Average Input Power I = ',Ivals[i], ': ',numpy.mean(data[1]), ' +/- ', 0.5*( numpy.max(data[1]) - numpy.min(data[1]) ), ' ( dBm )')
                    # Plot Loop Power Values versus VVOA
                    hv_data1.append([data[0], data[1]]); labels1.append('P$_{1}$ I = %(v1)d (mA)'%{"v1":Ivals[i]}); marks1.append(Plotting.labs_dashed[i]); 
                    hv_data1.append([data[0], data[2]]); labels1.append('P$_{2}$ I = %(v1)d (mA)'%{"v1":Ivals[i]}); marks1.append(Plotting.labs[i]); 
                    
                    hv_data2.append([data[0], data[3]]); labels2.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks2.append(Plotting.labs[i]); 

                # Make the Plot
                args = Plotting.plot_arg_multiple()

                args.loud = False
                args.crv_lab_list = labels1
                args.mrk_list = marks1
                args.x_label = 'VOA Bias (V)'
                args.y_label = 'Power (dBm)'
                args.fig_name = 'Input_Loop_Power'

                Plotting.plot_multiple_curves(hv_data1, args)

                args.crv_lab_list = labels2
                args.mrk_list = marks2
                args.x_label = 'VOA Bias (V)'
                args.y_label = 'Power Ratio P$_{2}$ / P$_{1}$'
                args.fig_name = 'Input_Loop_Power_Ratio'

                Plotting.plot_multiple_curves(hv_data2, args)

                os.chdir(DATA_HOME)
            
            # Make plots of the gathered summarised data
            PLOT_RES_FILES = True # Generate the plots of the summarised data files
            PLOT_VS_PRAT = True # Generate the plot with Power Ratio along the x-axis, other wise plot versus V_{VOA}
            
            if PLOT_RES_FILES:
                os.chdir(resDir)
                print(os.getcwd())
                # make a plot of various measured values versus Power Ratio
                # col 0: P1 / dBm col 1: P2 / dBm col 2: P2 / P1 col 3: Pmax / dBm col 4: LLest / units col 5: LLVfit / units col 6: LLLfit / units col 7: LL-20 / units col 8: LLVLor / units col 9: LLVGau / units col 10: RBW / units
                # 2. P1, P2 versus Power Ratio with Errors
                # 1. Pmax versus Power Ratio with Errors
                # 3. LLest versus Power Ratio with Errors
                # 4. LL-20 versus Power Ratio with Errors
                # 5. LLVfit versus Power Ratio with Errors
                # 6. Voigt_Lor_HWHM, LLest_-20 versus Power Ratio with Errors
                # 7. Voigt_Lor_HWHM, Voigt_Gau_Stdev versus Power Ratio with Errors
                
                Ivals = [100, 200, 300]
                #Ivals = [100]
                RBWVals = [50, 100, 250, 500]

                # Input powers for the NKT data set, June 2023
                #Pvals = [3.356, 9.313, 11.767]
                #Perr = [0.016, 0.015, 0.013]
                
                # Input powers for the NKT data set, February 2025
                #Pvals = [3.7265, 9.452, 11.879]
                #Perr = [0.015, 0.036, 0.025]
                
                # Input powers for the NKT data set, March 2025
                Pvals = [3.769, 9.519, 11.934]
                Perr = [0.016, 0.013, 0.025]

                RBWstr = '100Hz'
                LLMunitstr = 'kHz'

                # Input powers for the CoBrite data set
                #Pvals = [4.365, 5.512, 6.539]
                #Perr = [0.066, 0.011, 0.018]
                #RBWstr = '5kHz'
                #LLMunitstr = 'MHz'
                
                #VVOA = numpy.arange(2.8, 4.0, 0.2)
                #VVOA = numpy.arange(0, 2.6, 0.5)
                #VVOA = numpy.concatenate([numpy.arange(0, 2.6, 0.5), numpy.arange(2.8, 3.9, 0.2)] )
                VVOA = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
                Xvals = []
                LL_20_scale = 2.0*math.sqrt(99.0) # constant for converting LL-20 values into LL-Lorentzian values
                print(VVOA)
                hv_data1 = []; labels1 = []; marks1 = []
                hv_data2 = []; labels2 = []; marks2 = []
                hv_data3 = []; labels3 = []; marks3 = []
                hv_data4 = []; labels4 = []; marks4 = []
                hv_data44 = []; labels44 = []; marks44 = []
                hv_data5 = []; labels5 = []; marks5 = []
                hv_data55 = []; labels55 = []; marks55 = []
                hv_data6 = []; labels6 = []; marks6 = []
                hv_data66 = []; labels66 = []; marks66 = []
                hv_data7 = []; labels7 = []; marks7 = []
                hv_data77 = []; labels77 = []; marks77 = []
                for i in range(0, len(Ivals), 1):
                    esaResFileName = 'Measurement_Results_I_%(v1)d.txt'%{"v1":Ivals[i]}
                    esaErrFileName = 'Measurement_Errors_I_%(v1)d.txt'%{"v1":Ivals[i]}
                    data = numpy.loadtxt(esaResFileName, delimiter = '\t', unpack = True, skiprows = 1)
                    dataErr = numpy.loadtxt(esaErrFileName, delimiter = '\t', unpack = True, skiprows = 1)

                    print('Average Input Power I = ',Ivals[i], ': ',numpy.mean(data[0]), ' +/- ', 0.5*( numpy.max(data[0]) - numpy.min(data[0]) ), ' ( dBm )')

                    Xvals = data[2] if PLOT_VS_PRAT else VVOA

                    startVal = 0 # ignore the data at the start of the VVOA sweep? 
                    endVal = numpy.size(data[2])
                    #endVal = -1 + numpy.size(data[2]) # ignore the results of the V_{VOA} = 4V measurement, attenuation is too high, error bars too large, obscuring the result

                    # 1. Pmax versus Power Ratio with Errors
                    hv_data1.append([Xvals[startVal:endVal], data[3][startVal:endVal], numpy.absolute( 0.5*dataErr[3][startVal:endVal] ) ] ); labels1.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks1.append(Plotting.labs_lins[i%(len(Plotting.labs))])

                    # 2. P1, P2 versus Power Ratio with Errors
                    hv_data2.append([Xvals[startVal:endVal], data[0][startVal:endVal], 0.5*dataErr[0][startVal:endVal]]); labels2.append('P$_{1}$ I = %(v1)d (mA)'%{"v1":Ivals[i]}); marks2.append(Plotting.labs_lins[i%(len(Plotting.labs))])
                    hv_data2.append([Xvals[startVal:endVal], data[1][startVal:endVal], numpy.absolute( 0.5*dataErr[1][startVal:endVal] ) ]  ); labels2.append('P$_{2}$ I = %(v1)d (mA)'%{"v1":Ivals[i]}); marks2.append(Plotting.labs_dashed[i%(len(Plotting.labs))])

                    # 3. LLest versus Power Ratio with Errors
                    hv_data3.append([Xvals[startVal:endVal], data[4][startVal:endVal], 0.5*dataErr[4][startVal:endVal]]); labels3.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks3.append(Plotting.labs[i%(len(Plotting.labs))])

                    # 4. LL-20 versus Power Ratio with Errors
                    hv_data4.append([Xvals[startVal:endVal], data[7][startVal:endVal], 0.5*dataErr[7][startVal:endVal]]); labels4.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks4.append(Plotting.labs[i%(len(Plotting.labs))])
                    
                    hv_data44.append([Xvals[startVal:endVal], dataErr[7][startVal:endVal]]); labels44.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks44.append(Plotting.labs[i%(len(Plotting.labs))])

                    # 5. LLVfit versus Power Ratio with Errors
                    hv_data5.append([Xvals[startVal:endVal], data[5][startVal:endVal], 0.5*dataErr[5][startVal:endVal]]); labels5.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks5.append(Plotting.labs[i%(len(Plotting.labs))])
                    
                    hv_data55.append([Xvals[startVal:endVal], dataErr[5][startVal:endVal]]); labels55.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks55.append(Plotting.labs[i%(len(Plotting.labs))])

                    # 6. Voigt_Lor_HWHM, LLest_-20 versus Power Ratio with Errors
                    hv_data6.append([Xvals[startVal:endVal], data[8][startVal:endVal], 0.5*dataErr[8][startVal:endVal]]); labels6.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks6.append(Plotting.labs[i%(len(Plotting.labs))])
                    hv_data6.append([Xvals[startVal:endVal], data[7][startVal:endVal] / LL_20_scale, dataErr[7][startVal:endVal] / (2.0*LL_20_scale)]); labels6.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks6.append(Plotting.labs_dashed[i%(len(Plotting.labs))]) # LL-20 converted to LL-Lor data
                    
                    hv_data66.append([Xvals[startVal:endVal], dataErr[8][startVal:endVal]]); labels66.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks66.append(Plotting.labs[i%(len(Plotting.labs))])
                    hv_data66.append([Xvals[startVal:endVal], dataErr[7][startVal:endVal] / LL_20_scale]); labels66.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks66.append(Plotting.labs_dashed[i%(len(Plotting.labs))]) # LL-20 converted to LL-Lor data
                    
                    # 7. Voigt_Lor_HWHM, Voigt_Gau_Stdev versus Power Ratio with Errors
                    hv_data7.append([Xvals[startVal:endVal], data[8][startVal:endVal], 0.5*dataErr[8][startVal:endVal]]); labels7.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks7.append(Plotting.labs[i%(len(Plotting.labs))])
                    hv_data7.append([Xvals[startVal:endVal], data[9][startVal:endVal], 0.5*dataErr[9][startVal:endVal]]); labels7.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks7.append(Plotting.labs_dashed[i%(len(Plotting.labs))])
                    
                    hv_data77.append([Xvals[startVal:endVal], dataErr[8][startVal:endVal]]); labels77.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks77.append(Plotting.labs[i%(len(Plotting.labs))])
                    hv_data77.append([Xvals[startVal:endVal], dataErr[9][startVal:endVal]]); labels77.append('P$_{1}$ = %(v1)0.3f (dBm)'%{"v1":Pvals[i]}); marks77.append(Plotting.labs_dashed[i%(len(Plotting.labs))])

                DRAW_FULL_PLOT = True # Draw the figure over the whole range, otherwise draw the figure on the zoomed range

                # 1. Pmax versus Power Ratio with Errors
                args = Plotting.plot_arg_multiple()

                args.loud = False
                args.crv_lab_list = labels1
                args.mrk_list = marks1
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Spectral Peak Value (dBm / %(v1)s )'%{"v1":RBWstr}
                args.fig_name = 'Spectral_Peak_Value_vs_Prat' if PLOT_VS_PRAT else 'Spectral_Peak_Value_vs_VVOA'

                Plotting.plot_multiple_curves_with_errors(hv_data1, args)

                # 2. P1, P2 versus Power Ratio with Errors
                args.loud = False
                args.crv_lab_list = labels2
                args.mrk_list = marks2
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Optical Power ( dBm )'
                args.fig_name = 'Optical_Power_vs_Prat' if PLOT_VS_PRAT else 'Optical_Power_vs_VVOA'

                Plotting.plot_multiple_curves_with_errors(hv_data2, args)

                # 3. LLest versus Power Ratio with Errors
                args.loud = True
                args.crv_lab_list = labels3
                args.mrk_list = marks3
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Laser Linewidth ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth_vs_Prat' if PLOT_VS_PRAT else 'Laser_Linewidth_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves_with_errors(hv_data3, args)

                # 4. LL-20 versus Power Ratio with Errors
                args.loud = False
                args.crv_lab_list = labels4
                args.mrk_list = marks4
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Laser Linewidth at -20 dB ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth_20_vs_Prat' if PLOT_VS_PRAT else 'Laser_Linewidth_20_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 8, 14]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 8, 14] if DRAW_FULL_PLOT else [0, 0.4, 8, 14]
                #else:
                #    args.plt_range = [2.7, 3.9, 8, 14]

                Plotting.plot_multiple_curves_with_errors(hv_data4, args)

                # 44. LL-20 Error versus Power Ratio
                args.loud = False
                args.crv_lab_list = labels44
                args.mrk_list = marks44
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Laser Linewidth at -20 dB ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Error_Laser_Linewidth_20_vs_Prat' if PLOT_VS_PRAT else 'Error_Laser_Linewidth_20_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 8, 14]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 8, 14] if DRAW_FULL_PLOT else [0, 0.4, 8, 14]
                #else:
                #    args.plt_range = [2.7, 3.9, 8, 14]

                Plotting.plot_multiple_curves(hv_data44, args)

                # 5. LLVfit versus Power Ratio with Errors
                args.loud = True
                args.crv_lab_list = labels5
                args.mrk_list = marks5
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Laser Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth_Voigt_vs_Prat' if PLOT_VS_PRAT else 'Laser_Linewidth_Voigt_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves_with_errors(hv_data5, args)
                
                print('\nAverage linewidth over all VVOA variation')
                for i in range(0, len(hv_data5), 1): print('mean: ',numpy.mean(hv_data5[i][1]),' +/- ',0.5*(numpy.max(hv_data5[i][1]) - numpy.min(hv_data5[i][1]) ) )

                args.loud = False
                args.fig_name = 'Laser_Linewidth_Voigt_Lin_Fit_vs_Prat' if PLOT_VS_PRAT else 'Laser_Linewidth_Voigt_Lin_Fit_vs_VVOA'

                Plotting.plot_multiple_linear_fit_curves(hv_data5, args)

                # Linear fit to the LLVfit versus VVOA data sets
                # Is the slope the same in each case? No, not really
                #for i in range(0, len(hv_data5), 1):
                #    Common.linear_fit(hv_data5[i][0], hv_data5[i][1], [2.5, 2.5], True)
                
                # 55. LLVfit Error versus Power Ratio
                args.loud = False
                args.crv_lab_list = labels55
                args.mrk_list = marks55
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Laser Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Error_Laser_Linewidth_Voigt_vs_Prat' if PLOT_VS_PRAT else 'Error_Laser_Linewidth_Voigt_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves(hv_data55, args)

                # 6. Voigt_Lor_HWHM, LLest_-20 versus Power Ratio with Errors
                args.loud = True
                args.crv_lab_list = labels6
                args.mrk_list = marks6
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Intrinsic Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Intrinsic_Linewidth_Voigt_vs_Prat' if PLOT_VS_PRAT else 'Intrinsic_Linewidth_Voigt_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves_with_errors(hv_data6, args)

                # 66. Voigt_Lor_HWHM Error, LLest_-20 Error versus Power Ratio
                args.loud = False
                args.crv_lab_list = labels66
                args.mrk_list = marks66
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Intrinsic Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Error_Intrinsic_Linewidth_Voigt_vs_Prat' if PLOT_VS_PRAT else 'Error_Intrinsic_Linewidth_Voigt_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves(hv_data66, args)

                # 7. Voigt_Lor_HWHM, Voigt_Gau_Stdev versus Power Ratio with Errors
                args.loud = False
                args.crv_lab_list = labels7
                args.mrk_list = marks7
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Voigt Fit Parameters ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Voigt_Params_vs_Prat' if PLOT_VS_PRAT else 'Voigt_Params_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves_with_errors(hv_data7, args)
                
                # 77. Voigt_Lor_HWHM, Voigt_Gau_Stdev versus Power Ratio with Errors
                args.loud = False
                args.crv_lab_list = labels77
                args.mrk_list = marks77
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Voigt Fit Parameters ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Error_Voigt_Params_vs_Prat' if PLOT_VS_PRAT else 'Error_Voigt_Params_vs_VVOA'
                #args.plt_range = [2.7, 3.9, 1.5, 3.25]
                #if PLOT_VS_PRAT:
                #    args.plt_range = [0, 1.5, 1.5, 3.25] if DRAW_FULL_PLOT else [0, 0.4, 1.5, 3.25]
                #else:
                #    args.plt_range = [2.7, 3.9, 1.5, 3.25]

                Plotting.plot_multiple_curves(hv_data77, args)
            
            PLOT_VS_RBW = False # Make the analysis plots of the measured data versus RBW

            if PLOT_VS_RBW:
                os.chdir(resDir)
                print(os.getcwd())
                # make a plot of various measured values versus Power Ratio
                # col 0: P1 / dBm col 1: P2 / dBm col 2: P2 / P1 col 3: Pmax / dBm col 4: LLest / units col 5: LLVfit / units col 6: LLLfit / units col 7: LL-20 / units col 8: LLVGau / units col 9: LLVLor / units
                
                # 1. Pmax versus Power Ratio with Errors
                # 2. P1, P2 versus Power Ratio with Errors
                # 3. LLest versus Power Ratio with Errors
                # 4. LL-20 versus Power Ratio with Errors
                # 5. LLVfit versus Power Ratio with Errors

                Ival = 100
                RBWVals = [0.05, 0.1, 0.5, 0.5] # RBW in kHz
                FspanVals = [50, 100, 250, 500] # Fspan in kHz
                LLMunitstr = 'kHz'
                
                # Read in the data
                esaResFileName = 'Measurement_Results_I_%(v1)d.txt'%{"v1":Ival}
                esaErrFileName = 'Measurement_Errors_I_%(v1)d.txt'%{"v1":Ival}
                data = numpy.loadtxt(esaResFileName, delimiter = '\t', unpack = True, skiprows = 1)
                dataErr = numpy.loadtxt(esaErrFileName, delimiter = '\t', unpack = True, skiprows = 1)

                # Make the Plots
                args = Plotting.plot_arg_single()

                # 1. Pmax versus Power Ratio with Errors

                # 2. P1, P2 versus Power Ratio with Errors
                args.loud = False
                #args.curve_label = ''
                #args.mrk_list = marks5
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = 'Spectral Peak Value (dBm)'
                args.fig_name = 'Spectral_Peak_Value'
                args.plt_title = 'P$_{in}$ = 3.34 (dBm), P$_{rat}$ = 1.06, V$_{VOA}$ = 3V'
                args.plt_range = [0, 525, -42, -28]
                
                Plotting.plot_single_curve_with_errors(FspanVals, data[3], dataErr[3], args)

                # 3. LLest versus Power Ratio with Errors
                
                #args.curve_label = ''
                #args.mrk_list = marks5
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = 'Laser Linewidth ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth'
                args.plt_range = [0, 525, 1.0, 3]
                
                Plotting.plot_single_curve_with_errors(FspanVals, data[4], dataErr[4], args)

                # 4. LL-20 versus Power Ratio with Errors
                
                #args.curve_label = ''
                #args.mrk_list = marks5
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = 'Laser Linewidth at -20 dB ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth_20'
                args.plt_range = [0, 525, 9, 12]
                
                Plotting.plot_single_curve_with_errors(FspanVals, data[7], dataErr[7], args)

                # 5. LLVfit versus RBW with Errors
                
                #args.curve_label = ''
                #args.mrk_list = marks5
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = 'Laser Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth_Voigt'
                args.plt_range = [0, 525, 1.0, 3]
                
                Plotting.plot_single_curve_with_errors(FspanVals, data[5], dataErr[5], args)

                # Plot the estimated and fitted linewidths on the same graph
                hv_data = []; labels = []; marks = []
                hv_data.append([FspanVals, data[4], dataErr[4]]); labels.append('Estimated'); marks.append(Plotting.labs[0]); 
                hv_data.append([FspanVals, data[5], dataErr[5]]); labels.append('Voigt Fit'); marks.append(Plotting.labs[1]); 

                args = Plotting.plot_arg_multiple()

                args.loud = False
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = 'Laser Linewidth ( %(v1)s )'%{"v1":LLMunitstr}
                args.fig_name = 'Laser_Linewidth_Est_Voigt'
                args.plt_title = 'P$_{in}$ = 3.34 (dBm), P$_{rat}$ = 1.06, V$_{VOA}$ = 3V'
                args.plt_range = [0, 525, 1.0, 3]

                Plotting.plot_multiple_curves_with_errors(hv_data, args)

                # Make a plot of the sigma / RBW ratio versus span
                res_theor = 0.16 # theoretical LCR-DSHI resolution based on D_{eff} = 400km
                hv_data2 = []
                hv_data2.append([FspanVals, dataErr[4] / RBWVals])
                hv_data2.append([FspanVals, dataErr[5] / RBWVals])

                #print(dataErr[4], ',', RBWVals, ',', hv_data2[0][1])

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = '( Error / RBW ) Ratio'
                args.fig_name = 'Laser_Linewidth_Error_RBW_Ratio'
                args.plt_title = 'P$_{in}$ = 3.34 (dBm), P$_{rat}$ = 1.06, V$_{VOA}$ = 3V'
                args.plt_range = [0, 525, 0, 7]

                Plotting.plot_multiple_curves(hv_data2, args)

                # Make a plot of the sigma / theoretical-resolution ratio versus span
                res_theor = 0.16 # theoretical LCR-DSHI resolution based on D_{eff} = 400km
                hv_data3 = []
                hv_data3.append([FspanVals, dataErr[4] / res_theor])
                hv_data3.append([FspanVals, dataErr[5] / res_theor])

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Measurement Span ( kHz )'
                args.y_label = '( Error / Res ) Ratio'
                args.fig_name = 'Laser_Linewidth_Error_Res_Ratio'
                args.plt_title = 'P$_{in}$ = 3.34 (dBm), P$_{rat}$ = 1.06, V$_{VOA}$ = 3V'
                args.plt_range = [0, 525, 0, 7]

                Plotting.plot_multiple_curves(hv_data3, args)
            
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Parse_ESA_Settings(DATA_HOME, loud = False):

    # Read the ESA Settings file and extract the measurement power settings
    # Output is dictionary of the form [ Input Power (dBm), Loop Power (dBm), Loop / Input Ratio, VOA Bias (V) ]
    # R. Sheehan 6 - 6 - 2023

    FUNC_NAME = ".Parse_ESA_Settings()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            thePath = 'ESA_Settings.txt'
            if glob.glob(thePath):
                theFile = open(thePath,'r')
                theData = theFile.readlines() # read the data from the file
                line_list = [2, 3, 10, 11, 12, 13]
                theVals = []
                theLabels = ['FSpan', 'RBW', 'P1', 'P2', 'P2/P1', 'VVoa']
                count = 0
                for lines in theData: 
                    if count in line_list:
                        if loud: print( Common.extract_values_from_string(lines) )
                        if count == 2 or count == 3:
                            if loud: print( float(Common.extract_values_from_string(lines)[0]) * 10**float(Common.extract_values_from_string(lines)[1]) )
                            theVals.append( float(Common.extract_values_from_string(lines)[0]) * 10**float(Common.extract_values_from_string(lines)[1]) )
                        else:
                            theVals.append( float( Common.extract_values_from_string(lines)[-1] ) )
                    count = count + 1
                resDict = dict( zip( theLabels, theVals ) ) # make the dictionary
                return resDict
            else:
                ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate: ' + thePath
                raise Exception
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate: ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Parse_Results_Summary(DATA_HOME, errorIsstdev = True, loud = False):

    # Read the Results Summary files and extract various values
    # errorIsstdev decides whether or not you want the error to be expressed in terms of the standard deviation or the data range
    # Output is two dictionaries one for the values, one for the errors
    # Output is of the form ['Pmax/dBm', 'LLest', 'LL_Vfit', 'LL_Lfit', 'LLest_-20', 'Voigt_Lor_HWHM', 'Voigt_Gau_Stdev', 'P1/dBm', 'P2/dBm', 'P2/P1']
    # R. Sheehan 6 - 6 - 2023

    FUNC_NAME = ".Parse_Results_Summary()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            thePath = 'ResultsSummary.txt'
            if glob.glob(thePath):
                theFile = open(thePath,'r')
                theData = theFile.readlines() # read the data from the file
                line_list = [5, 6, 7, 8, 9, 14, 15, 28, 29, 30]
                theLabels = ['Pmax/dBm', 'LLest', 'LL_Vfit', 'LL_Lfit', 'LLest_-20', 'Voigt_Lor_HWHM', 'Voigt_Gau_Stdev', 'P1/dBm', 'P2/dBm', 'P2/P1']
                theVals = []
                theErrs = []
                count = 0
                for lines in theData:
                    if count in line_list:
                        if loud: print(Common.extract_values_from_string(lines))
                        
                        # Extract the mean value of the parameter
                        if count == 9 or count == 28 or count == 29: pos = 1
                        elif count == 30: pos = 2
                        else: pos = 0
                        theVals.append( float ( Common.extract_values_from_string(lines)[pos] ) )
                        
                        if errorIsstdev:
                            # Use standard deviation of measured distribution as the error estimate, massive overestimation of error
                            if count == 9 or count == 28 or count == 29: pos = 2
                            elif count == 30: pos = 3
                            else: pos = 1
                        else:
                            # Use data range as the error estimate, massive overestimation of error
                            if count == 9 or count == 28 or count == 29: pos = 5
                            elif count == 30: pos = 6
                            else: pos = 4
                            
                        theErrs.append( float ( Common.extract_values_from_string(lines)[pos] ) )

                    count = count + 1
                resDict = dict( zip( theLabels, theVals ) ) # make the dictionary for the values
                errDict = dict( zip( theLabels, theErrs ) ) # make the dictionary for the errors
                return [resDict, errDict]
            else:
                ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate: ' + thePath
                raise Exception
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate: ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Lineshape_FFTs():

    # Examine the FFT of lineshapes as a function of beat frequency / effective distance
    # R. Sheehan 26 - 2 - 2024

    FUNC_NAME = ".Lineshape_FFTs()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:

        Ival = 200
        loopLength = 50

        # CoBrite Parameters
        theLaser = 'CoBriteTLS'
        temperature = 25        
        RBW = '5kHz' # RBW used in the measurement
        FUnits = ' / MHz'
        LWUNits = ' / MHz / ' + RBW
        Pin = 0.5*(4.77 + 4.72) # optical input power for measurement
        Prat = 0.5*(0.075 + 0.323) # Loop power ratio

        # NKT Parameters
        #theLaser = 'NKT'
        #temperature = 35        
        #RBW = '100Hz' # RBW used in the measurement
        #FUnits = ' / kHz'
        #LWUNits = ' / kHz / ' + RBW
        #Pin = 0.5*(9.71 + 9.59) # optical input power for measurement
        #Prat = 0.5*(0.082 + 0.107) # Loop power ratio

        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Beat_Note_Lineshapes/'%{"v2":theLaser, "v3":temperature, "v4":loopLength}

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # CoBrite Laser
            looplength = 10; Nbeats = (1360/80);             
            #looplength = 50; Nbeats = (960/80); 

            # NKT Laser
            #looplength = 10; Nbeats = (1280/80);             
            #looplength = 50; Nbeats = (1120/80); 

            F_AOM = 80            
            fbeats = numpy.arange(F_AOM, Nbeats*F_AOM + 1, F_AOM)
            distances = numpy.arange(looplength, Nbeats*looplength + 1, looplength)

            filestr = 'Lineshape_I_200_D_%(v1)d_fb_%(v2)d.txt'

            # Plot the measured lineshapes along the beat notes
            #Plot_Lineshape_Vs_Fbeat(filestr, looplength, theLaser, fbeats, distances, LWUNits)

            # Plot the measured lineshapes together
            #Plot_Lineshape_Together(filestr, looplength, theLaser, fbeats, distances, FUnits, LWUNits, Pin, Prat)

            # Plot the computed FFT together
            filestr_X = 'Lineshape_I_200_D_%(v1)d_fb_%(v2)d_Frq_data.txt'
            filestr_Y = 'Lineshape_I_200_D_%(v1)d_fb_%(v2)d_FFT_data.txt'
            Plot_FFT_Together(filestr_X, filestr_Y, looplength, theLaser, fbeats, distances, FUnits, LWUNits, Pin, Prat)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Lineshape_FFTs_Comparison():
    # Compare the computed lineshapes for the CoBrite TLS and the NKT Fibre Laser on the same graph
    # Don't need an exhaustive set of plots, just compare the data from the D = 10km, fb = 800MHz, Deff = 100km
    # R. Sheehan 4 - 3 - 2024

    FUNC_NAME = ".Lineshape_FFTs_Comparison()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Lineshape files
            lineshape_file = 'Lineshape_I_200_D_10_fb_800.txt' # the lineshape
            lineshape_fft_X = 'Lineshape_I_200_D_10_fb_800_Frq_Data.txt' # FFT of the lineshape, X-values
            lineshape_fft_Y = 'Lineshape_I_200_D_10_fb_800_FFT_Data.txt' # FFT of the lineshape, Y-values

            # Goto Cobrite Directory and Fetch the data you want
            Ival = 200
            loopLength = 50

            lineshapes = []
            lineshapes_FFT = []
            labels = []
            marks = []

            # CoBrite Parameters
            theLaser = 'CoBriteTLS'
            temperature = 25        
            RBW = '5kHz' # RBW used in the measurement
            FUnits = ' / MHz'
            LWUNits = ' / MHz / ' + RBW
            Pin = 0.5*(4.77 + 4.72) # optical input power for measurement
            Prat = 0.5*(0.075 + 0.323) # Loop power ratio

            SUB_DIR = 'LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Beat_Note_Lineshapes/'%{"v2":theLaser, "v3":temperature, "v4":loopLength}
            os.chdir(SUB_DIR)
            print(os.getcwd())
            CoBrite_lineshape = numpy.loadtxt(lineshape_file, delimiter = '\t')
            lineshapes.append([1000.0*(CoBrite_lineshape[0]-800.0), CoBrite_lineshape[1]]); labels.append('CoBrite 5kHz/2MHz'); marks.append(Plotting.labs_lins[0])
            time_data = numpy.loadtxt(lineshape_fft_X, delimiter = '\t')
            fft_data = numpy.loadtxt(lineshape_fft_Y, delimiter = ',', unpack = True)
            # scale the abs(FFT) so that its maximum is at 1
            scale_factor = numpy.max(fft_data[2])
            lineshapes_FFT.append( [1000.0*time_data, fft_data[2] / scale_factor] ); # interested in plotting the abs(FFT) with time in units of us
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Goto NKT Directory and Fetch the data you want

            # NKT Parameters
            theLaser = 'NKT'
            temperature = 35        
            RBW = '100Hz' # RBW used in the measurement
            FUnits = ' / kHz'
            LWUNits = ' / kHz / ' + RBW
            Pin = 0.5*(9.71 + 9.59) # optical input power for measurement
            Prat = 0.5*(0.082 + 0.107) # Loop power ratio

            SUB_DIR = 'LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Beat_Note_Lineshapes/'%{"v2":theLaser, "v3":temperature, "v4":loopLength}
            os.chdir(SUB_DIR)
            print(os.getcwd())
            NKT_lineshape = numpy.loadtxt(lineshape_file, delimiter = '\t')
            lineshapes.append(NKT_lineshape); labels.append('NKT 100Hz/100kHz'); marks.append(Plotting.labs_lins[1])
            time_data = numpy.loadtxt(lineshape_fft_X, delimiter = '\t')
            fft_data = numpy.loadtxt(lineshape_fft_Y, delimiter = ',', unpack = True)
            # scale the abs(FFT) so that its maximum is at 1
            scale_factor = numpy.max(fft_data[2])
            lineshapes_FFT.append( [1000.0*time_data, fft_data[2] / scale_factor] ); # interested in plotting the abs(FFT) with time in units of us

            #Store the Plot in the NKT Directory
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.show_leg = True
            args.mrk_list = marks
            args.x_label = 'Frequency' + FUnits
            args.y_label = 'Power / dBm'
            args.fig_name = 'Lineshapes_Comparison_D_10_fb_800'
            args.plt_title = 'D$_{eff}$ = 100km, P$_{CoBr}$ = 4.74dBm, P$_{NKT}$ = 9.65dBm'
            args.plt_range = [-300, 300, -80, -40]

            Plotting.plot_multiple_curves(lineshapes, args)

            args.loud = True
            args.crv_lab_list = labels
            args.show_leg = True
            args.mrk_list = marks
            args.log_x = False
            args.x_label = 'Time / us'
            args.y_label = 'FFT(Lineshape)'
            args.fig_name = 'Lineshapes_FFT_Comparison_D_10_fb_800'
            args.plt_title = 'D$_{eff}$ = 100km, P$_{CoBr}$ = 4.74dBm, P$_{NKT}$ = 9.65dBm'
            args.plt_range = [0, 100, 0, 1]

            Plotting.plot_multiple_curves(lineshapes_FFT, args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Lineshape_Vs_Fbeat(filestr, looplength, theLaser, fbeats, distances, LWUNits):

    # Make a plot of all the lineshapes placed at their respective fbeat values, scale all freq values to MHz
    # filestr is the template for the filename containing the linehsape data
    # looplength is the length of the fibre loop used in the measurement
    # theLaser is the name of the DUT
    # fbeats is an array of beat notes from the measurement system, in units of MHz
    # distances is an array of effective loop lengths corresponding to fbeats, in units of km
    # LWUNits is the string containing the ESA RBW data for the system
    # R. Sheehan 27 - 2 - 2024

    FUNC_NAME = ".Plot_Lineshape_Vs_Fbeat()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Plot the measured lineshapes together
        hv_data = []; marks = []; labels = []; 
        ord = 'Frequency'
        count = 0
        for f in fbeats:
            filename = filestr%{"v1":looplength, "v2":f}
            if glob.glob(filename):
                data = numpy.loadtxt(filename, delimiter = '\t')
                if theLaser == 'NKT':
                    data[0] = (data[0]/1000.0) + f # offset the frequency data by fbeat, change funits from kHz to MHz
                hv_data.append(data); 
                marks.append(Plotting.labs_lins[count%len(Plotting.labs_lins)]); labels.append( 'f$_{b}$ = %(v1)d MHz'%{"v1":f} )
                count = count + 1

        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.show_leg = False
        args.mrk_list = marks
        args.x_label = 'Beat Frequency / MHz'
        args.x_label_2 = 'Effective Loop Length / km'
        args.y_label = 'Power / dBm' + LWUNits
        args.xold = fbeats
        args.xnew = distances
        args.fig_name = 'Lineshapes_vs_%(v1)s_D_%(v2)d'%{"v1":ord, "v2":looplength}
        #args.plt_title = '%(v1)s, P$_{1}$ = %(v2)0.2f dBm, P$_{2}$ / P$_{1}$ = %(v3)0.2f, L$_{fbr}$ = %(v4)d km'%{"v1":theLaser, "v2":Pin, "v3":Prat, "v4":looplength}
        args.plt_range = [0, 1440, -100, -30]

        Plotting.plot_two_x_axis(hv_data, args)

        del hv_data; del marks; del labels; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Lineshape_Together(filestr, looplength, theLaser, fbeats, distances, FUnits, LWUNits, Pin, Prat, SubCoher = False):

    # Make a plot of all the lineshapes centred at 0kHz, scale all freq values to kHz
    # filestr is the template for the filename containing the linehsape data
    # looplength is the length of the fibre loop used in the measurement
    # theLaser is the name of the DUT
    # fbeats is an array of beat notes from the measurement system, in units of MHz
    # distances is an array of effective loop lengths corresponding to fbeats, in units of km
    # LWUNits is the string containing the ESA RBW data for the system
    # R. Sheehan 27 - 2 - 2024

    FUNC_NAME = ".Plot_Lineshape_Together()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Plot the measured lineshapes together
        hv_data = []; marks = []; labels = []; 
        ord = 'Frequency'
        count = 0
        for i in range(0, 6, 1):
            filename = filestr%{"v1":looplength, "v2":fbeats[i]}
            if glob.glob(filename):
                data = numpy.loadtxt(filename, delimiter = '\t')
                if theLaser == 'CoBriteTLS':
                    data[0] = data[0] - fbeats[i] # rescale the freq data from kHz to MHz and subtract the beat note value
                hv_data.append(data); 
                marks.append(Plotting.labs_lins[count%len(Plotting.labs_lins)]); labels.append( '%(v1)d km'%{"v1":distances[i]} )
                count = count + 1

        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.show_leg = True
        args.mrk_list = marks
        args.x_label = 'Frequency' + FUnits
        args.y_label = 'Power / dBm' + LWUNits
        args.fig_name = 'Lineshapes_Together_D_%(v2)d_SubCoher_Zoom'%{"v1":ord, "v2":looplength} if SubCoher else 'Lineshapes_Together_D_%(v2)d'%{"v1":ord, "v2":looplength}
        args.plt_title = '%(v1)s, P$_{1}$ = %(v2)0.2f dBm, P$_{2}$ / P$_{1}$ = %(v3)0.2f, L$_{fbr}$ = %(v4)d km'%{"v1":theLaser, "v2":Pin, "v3":Prat, "v4":looplength}
        args.plt_range = [-30, 30, -70, -10]

        Plotting.plot_multiple_curves(hv_data, args)

        del hv_data; del marks; del labels; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_FFT_Together(filestr_X, filestr_Y, looplength, theLaser, fbeats, distances, FUnits, LWUNits, Pin, Prat, SubCoher = False):

    # Make a plot of all the lineshapes centred at 0kHz, scale all freq values to kHz
    # filestr_X is the template for the filename containing the time values from the computed FFT(lineshape)
    # filestr_Y is the template for the filename containing the FFT values from the computed FFT(lineshape)
    # data is contained in the form real(FFT), imag(FFT), abs(FFT), arg(FFT)
    # all positive and negative components have been computed
    # looplength is the length of the fibre loop used in the measurement
    # theLaser is the name of the DUT
    # fbeats is an array of beat notes from the measurement system, in units of MHz
    # distances is an array of effective loop lengths corresponding to fbeats, in units of km
    # LWUNits is the string containing the ESA RBW data for the system
    # R. Sheehan 27 - 2 - 2024

    FUNC_NAME = ".Plot_FFT_Together()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Plot the measured lineshapes together
        hv_data = []; marks = []; labels = []; 
        ord = 'Frequency'
        count = 0
        for i in range(0, len(fbeats), 3):
            filename_X = filestr_X%{"v1":looplength, "v2":fbeats[i]}
            filename_Y = filestr_Y%{"v1":looplength, "v2":fbeats[i]}
            if glob.glob(filename_X) and glob.glob(filename_Y):
                time_data = numpy.loadtxt(filename_X, delimiter = '\t')
                fft_data = numpy.loadtxt(filename_Y, delimiter = ',', unpack = True)
                # scale the abs(FFT) so that its maximum is at 1
                scale_factor = numpy.max(fft_data[2])
                hv_data.append([1000.0*time_data, fft_data[2] / scale_factor]); # interested in plotting the abs(FFT) with time in units of us
                marks.append(Plotting.labs_lins[count%len(Plotting.labs_lins)]); labels.append( '%(v1)d km'%{"v1":distances[i]} )
                count = count + 1

        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.show_leg = True
        args.mrk_list = marks
        args.log_x = True
        args.x_label = 'Time / us'
        args.y_label = 'FFT(Lineshape)'
        args.fig_name = 'AutoCorr_D_%(v2)d_SubCoher'%{"v2":looplength} if SubCoher else 'AutoCorr_D_%(v2)d'%{"v2":looplength}
        args.plt_title = '%(v1)s, P$_{1}$ = %(v2)0.2f dBm, P$_{2}$ / P$_{1}$ = %(v3)0.2f, L$_{fbr}$ = %(v4)d km'%{"v1":theLaser, "v2":Pin, "v3":Prat, "v4":looplength}
        #args.plt_range = [0, 100, 0, 1]

        Plotting.plot_multiple_curves(hv_data, args)

        del hv_data; del marks; del labels; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def CNR_Analysis():

    # Plot the measured CNR data
    # R. Sheehan 11 - 3 - 2024

    FUNC_NAME = ".CNR_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Ival = 200
        Deff = 200

        # CoBrite Parameters
        # theLaser = 'CoBriteTLS'
        # temperature = 25        
        # RBW = '5kHz' # RBW used in the measurement
        # FUnits = ' / MHz'
        # LWUNits = ' / MHz / ' + RBW
        # Pin = 4.91 # optical input power for measurement

        # NKT Parameters
        theLaser = 'NKT'
        temperature = 35        
        RBW = '100Hz' # RBW used in the measurement
        FUnits = ' / kHz'
        
        #Pin = 6.19 # optical input power for measurement
        Pin = 9.5 # optical input power for measurement

        #DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Lineshape_vs_VOA/'%{"v2":theLaser, "v3":temperature, "v4":Deff}
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/CNR_Meas_6_3_2025/'%{"v2":theLaser, "v3":temperature, "v4":Deff}

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #filestr = 'Lineshape_VVOA_%(v1)d.txt'
            filestr = 'Lineshape_NKT_T_35_I_200_VVOA_%(v1)d.txt'
            #VVOA = [0, 1, 2, 3, 32, 34, 35, 36, 37, 38]
            #VVOA_vals = [0, 1, 2, 3, 3.2, 3.4, 3.5, 3.6, 3.7, 3.8]
            #VVOA = [0, 1, 2, 3, 35, 37]
            #VVOA_vals = [0, 1, 2, 3, 3.5, 3.7]
            #Fbeat = 640
            VVOA = [0, 1, 2, 3, 32, 35, 37]
            VVOA_vals = [0, 1, 2, 3, 3.2, 3.5, 3.7]
            Fbeat = 320

            LWUNits = ' / ' + RBW
            Plot_Lineshape_vs_VVOA(filestr, Deff, VVOA, VVOA_vals, Fbeat, theLaser, FUnits, LWUNits, Pin, True)

            #filename = 'NKT_CNR_VVOA_3.txt'
            filename = 'CNR_vs_VVOA_NKT_T_35_I_200.txt'
            LWUNits = ' / kHz / ' + RBW
            #Plot_CNR(filename, Deff, Fbeat, theLaser, FUnits, LWUNits, Pin)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Lineshape_vs_VVOA(filestr, looplength, VVOA, VVOA_vals, Fbeat, theLaser, FUnits, LWUNits, Pin, ScaleVert = False):

    # Make a plot of all the lineshapes centred at 0kHz, scale all freq values to kHz
    # filestr is the template for the filename containing the linehsape data
    # looplength is the length of the fibre loop used in the measurement
    # theLaser is the name of the DUT
    # VVOA is an array of VOA voltages used
    # Fbeat is the beat note used to make the measurement
    # LWUNits is the string containing the ESA RBW data for the system
    # R. Sheehan 27 - 2 - 2024

    FUNC_NAME = ".Plot_Lineshape_vs_VVOA()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Plot the measured lineshapes together
        hv_data = []; marks = []; labels = []; 
        ord = 'Frequency'
        count = 0
        for i in range(0, len(VVOA), 1):
            filename = filestr%{"v1":VVOA[i]}
            if glob.glob(filename):
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = False)
                # if theLaser == 'NKT':
                #     data[0] = 1000.0*(data[0] - Fbeat) # rescale the freq data from kHz to MHz and subtract the beat note value
                # else:
                #     data[0] = (data[0] - Fbeat) # rescale the freq data from kHz to MHz and subtract the beat note value
                if ScaleVert:
                    Ymax = numpy.max(data[1])
                    data[1] = data[1] - Ymax
                hv_data.append(data); 
                marks.append(Plotting.labs_lins[count%len(Plotting.labs_lins)]); 
                #labels.append( '%(v1)0.1f V'%{"v1":VVOA_vals[i]} )
                labels.append( '%(v1)0.1f V'%{"v1":VVOA_vals[i]} )
                count = count + 1

        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.show_leg = True
        args.mrk_list = marks
        args.x_label = 'Frequency' + FUnits
        args.y_label = 'Power / dBm' + LWUNits
        args.fig_name = 'Lineshapes_Together_D_%(v2)d'%{"v2":looplength} if ScaleVert == False else 'Lineshapes_Together_D_%(v2)d_Scaled'%{"v2":looplength}
        #args.plt_title = '%(v1)s, P$_{1}$ = %(v2)0.2f dBm, D$_{eff}$ = %(v4)d km'%{"v1":theLaser, "v2":Pin, "v4":looplength}
        if ScaleVert:
            args.plt_range = [-50, 50, -40, 0] if theLaser == 'NKT' else [-1, 1, -30, 0]
        else:
            args.plt_range = [-50, 50, -90, -20] if theLaser == 'NKT' else [-1, 1, -100, -30]

        Plotting.plot_multiple_curves(hv_data, args)

        del hv_data; del marks; del labels; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_CNR(filename, looplength, Fbeat, theLaser, FUnits, LWUNits, Pin):

    # Plot the CNR for a given laser

    FUNC_NAME = ".Plot_CNR()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(filename):
            data = numpy.loadtxt(filename, delimiter = '\t', unpack = True)

            args = Plotting.plot_arg_single()
            args.loud = True
            args.x_label = 'VOA Voltage / V'
            args.y_label = 'CNR / dB / 100Hz'
            args.fig_name = '%(v1)s_CNR_D_%(v2)d'%{"v1":theLaser,"v2":looplength}
            #args.plt_title = '%(v1)s, P$_{1}$ = %(v2)0.2f dBm, D$_{eff}$ = %(v4)d km'%{"v1":theLaser, "v2":Pin, "v4":looplength}
            args.plt_range = [0, 4, 20, 32] if theLaser == 'NKT' else [0, 4, 14, 24]

            Plotting.plot_single_curve_with_errors(data[0], data[1], 0.5*data[2], args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate file: ' + filename
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OL_Laser_Analysis():
    
    # Plot the data from the measurements for Odhran Liston's Laser
    # 25 - 10 - 2024

    FUNC_NAME = ".OL_Laser_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Odhran_Liston_LLM_10_2024/'
        
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Optical Spectra
            PLOT_OPTICAL = True
            
            if PLOT_OPTICAL:
                filenames = ['CoBrite_Laser_Spctrm_l_1554.txt',
                             #'OL_Laser_Spctrm_l_1554.txt',
                             #'OL_Laser_Spctrm_l_1554_Time_T2_NoAmp.txt',
                             #'OL_Laser_Spctrm_l_1554_Time_T2_WithAmp.txt',
                             'OL_Laser_Spctrm_l_1554_Time_T2_WithAmp_WithFilt.txt'#,
                             #'OL_Laser_Spctrm_l_1554_Time_T3_WithAmp_WithFilt.txt'
                             ]
                
                labels = ['CoBrite TLS',
                          #'OL T$_{1}$ No Amp',
                          #'OL T$_{2}$ No Amp',
                          #'OL T$_{2}$ Amp',
                          'OL T$_{2}$ Amp + Filt'#,
                          #'OL T$_{3}$ Amp + Filt'
                          ]
                
                hv_data = []
                marks = []
                for i in range(0, len(filenames),1):
                    data = numpy.loadtxt(filenames[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    #marks.append(Plotting.labs_lins[i%len(Plotting.labs_lins)])
                    
                marks = [Plotting.labs_lins[0], Plotting.labs_lins[2]]
                    
                # plot the data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Wavelength (nm)'
                args.y_label = 'Power / dBm / 0.05 nm'
                args.plt_range = [1552, 1556, -45, 10]
                args.fig_name = 'Optical_Spectra_Zoom_2'
                #args.plt_title = 'JDSU CQF915/508 $I_{DFB}$ = 200 mA'                
                            
                Plotting.plot_multiple_curves(hv_data, args)
                
            # ESA Spectrum
            PLOT_FULL_ESA = False    
            
            if PLOT_FULL_ESA:
                filenames =['OL_Amp_Filt_ESA_Spctrm_Full_1.txt','OL_Amp_Filt_ESA_Spctrm_Full_2.txt']
                labels = ['V$_{VOA}$ = 0V', 'V$_{VOA}$ = 3.5V']
                
                hv_data = []
                marks = []
                for i in range(0, len(filenames),1):
                    data = numpy.loadtxt(filenames[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append(Plotting.labs_lins[i%len(Plotting.labs_lins)])
                    
                # plot the data
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency (MHz)'
                args.y_label = 'Power / dBm / 100 kHz'
                #args.plt_range = [1552, 1556, -50, 10]
                args.fig_name = 'Full_ESA_Spectrum'
                #args.plt_title = 'JDSU CQF915/508 $I_{DFB}$ = 200 mA'                
                            
                Plotting.plot_multiple_curves(hv_data, args)

            # OE Waves Analysis
            PLOT_OE = False
            
            if PLOT_OE:
                filenames = ['OEWaves_Test_WithAmp_WithFilt_WithAtt_1.txt','OEWaves_Test_WithAmp_WithFilt_WithAtt_2.txt','OEWaves_Test_WithAmp_WithFilt_WithAtt_3.txt']
                
                lasname = 'OL_Laser'
                
                #for f in filenames: OEWaves_Analysis_Single(f, True)
                OEWaves_FNPSD_Multiple(filenames, lasname, True)
                OEWaves_FNPSD_Integration(filenames, lasname, True)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Lineshape_Comparison():

    # Plot the DFB, CoBrite and NKT lineshapes together on the same graph
    # Show the freq axis in log scale
    # R. Sheehan 8 - 11 - 2024

    FUNC_NAME = ".Lineshape_Comparison()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/'
        
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())
            
            # DFB Data centred at 80MHz
            dfbFile = 'LCR_DSHI_JDSU_DFB_T_20_D_400/LLM_Data_Nmeas_200_I_70_22_02_2024_13_59/Voigt_Average.txt'
            dfbData = numpy.loadtxt(dfbFile, delimiter = ',',unpack=True)
            #dfbData[0] = dfbData[0] + 560 # reset freq scale to 640MHz
            dfbData[0] = dfbData[0] - 80 # reset freq scale to 0MHz
            # convert freq data to log scale
            # for i in range(0, len(dfbData[0]), 1):
            #     dfbData[0][i] = math.log10(dfbData[0][i])
            dfbMax = numpy.max(dfbData[1]) # rescale peak value to 1
            dfbData[1] = dfbData[1] / dfbMax
            
            # CoBrite Data centred at 640MHz
            coBriteFile = 'LCR_DSHI_CoBriteTLS_T_25_D_400/LLM_Data_Nmeas_200_I_200_05_07_2023_11_00/Voigt_Average.txt'
            coBriteData = numpy.loadtxt(coBriteFile, delimiter = ',',unpack=True)
            coBriteData[0] = coBriteData[0] - 640 # reset freq scale to 0MHz
            #coBriteData[0] = 1000*coBriteData[0] # reset freq scale to kHz
            # convert freq data to log scale
            # for i in range(0, len(coBriteData[0]), 1):
            #     coBriteData[0][i] = math.log10(coBriteData[0][i])
            coBriteMax = numpy.max(coBriteData[1]) # rescale peak value to 1
            coBriteData[1] = coBriteData[1] / coBriteMax

            # NKT Data centred at 640MHz but rescaled to 0kHz
            NKTFile = 'LCR_DSHI_NKT_T_35_D_400/LLM_Data_Nmeas_200_I_200_20_06_2023_15_31/Voigt_Average.txt'
            NKTData = numpy.loadtxt(NKTFile, delimiter = ',',unpack=True)
            #NKTData[0] = 640 + (NKTData[0]/1000)  # reset freq scale to 640MHz
            NKTData[0] = (NKTData[0]/1000)  # reset freq scale to 0MHz
            # convert freq data to log scale
            # for i in range(0, len(NKTData[0]), 1):
            #     NKTData[0][i] = math.log10(NKTData[0][i])
            NKTMax = numpy.max(NKTData[1]) # rescale peak value to 1
            NKTData[1] = NKTData[1] / NKTMax
            
            hv_data = [dfbData, coBriteData, NKTData]
            marks = [Plotting.labs_lins[0], Plotting.labs_lins[1], Plotting.labs_lins[2]]
            labels = [r'DFB $\Delta\nu$ = 2.5 MHz', r'TLS $\Delta\nu$ = 100 kHz', r'NKT $\Delta\nu$ = 2 kHz']
            
            # hv_data = [coBriteData, NKTData]
            # marks = [Plotting.labs_lins[1], Plotting.labs_lins[2]]
            # labels = [r'TLS $\Delta\nu$ = 100 kHz', r'NKT $\Delta\nu$ = 2 kHz']

            # Make a plot of the measured data
            args = Plotting.plot_arg_multiple()
            
            args.crv_lab_list=labels
            args.mrk_list=marks
            args.loud = True
            args.x_label = 'Frequency ( MHz )'
            args.y_label = 'Fitted Lineshapes ( A. U. )'
            args.log_y = True
            args.plt_range = [-5, 5, 1e-2, 1]
            args.fig_name = 'LCR_DSHI_Report/Linewidths_compar1'
            
            Plotting.plot_multiple_curves(hv_data, args)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Pub_Figs():
    
    # Method for making publication figures
    # R. Sheehan 7 - 3 - 2025

    FUNC_NAME = ".Pub_Figs()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME
    
    try:

        PAPER_HOME = 'C:/Users/robertsheehan/Research/Publications/LCRDSHI_LLM/'

        if os.path.isdir(PAPER_HOME):
            os.chdir(PAPER_HOME)
            print(os.getcwd())

            PLOT_CNR = True

            if PLOT_CNR:
                #Deff = [200, 400]
                Deff = [200]
                theLaser = 'NKT'
                temperature = 35    
                RBW = '100Hz' # RBW used in the measurement
                FUnits = ' / kHz'
                LWUNits = ' / ' + RBW

                PLOT_VS_PRAT = False # Generate the plot with Power Ratio along the x-axis, otherwise plot versus V_{VOA}
                
                # Plot both CNR together
                hv_data = []; marks = []; labs = []; 
                
                for i in range(0, len(Deff), 1):
                    thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/CNR_Meas_6_3_2025/CNR_vs_VVOA_NKT_T_35_I_200.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[i]}
                    thedata = numpy.loadtxt(thefile, delimiter = '\t', unpack = True) if i==0 else numpy.loadtxt(thefile, delimiter = '\t', unpack = True, max_rows = 20)
                    #thedata[2] = 0.5*thedata[2]
                    
                    # Make a plot of the Prat vs VVOA
                    args = Plotting.plot_arg_single()
                    
                    args.loud = True
                    args.x_label = 'VOA Bias (V)'
                    args.y_label = 'Power Ratio P$_{2}$ / P$_{1}$'
                    args.curve_label = 'P$_{1}$ = 9.5 dBm'
                    args.fig_name = 'Prat_vs_Vvoa'
                    
                    Plotting.plot_single_curve(thedata[0], Compute_Prat(thedata[0]), args)

                    if PLOT_VS_PRAT:
                        thedata[0] = Compute_Prat(thedata[0])
                        
                    hv_data.append(thedata); labs.append('D = %(v1)d km'%{"v1":Deff[i]}); marks.append(Plotting.labs[i])

                args = Plotting.plot_arg_multiple()
                args.loud = True
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'CNR / dB / 100Hz'
                args.crv_lab_list = labs
                args.mrk_list = marks
                #args.fig_name = '%(v1)s_CNR_vs_Prat'%{"v1":theLaser} if PLOT_VS_PRAT else '%(v1)s_CNR_vs_VVOA'%{"v1":theLaser}
                args.fig_name = '%(v1)s_CNR_vs_Prat_D_200'%{"v1":theLaser} if PLOT_VS_PRAT else '%(v1)s_CNR_vs_VVOA_D_200'%{"v1":theLaser}
                #args.plt_title = '%(v1)s, P$_{1}$ = %(v2)0.2f dBm, D$_{eff}$ = %(v4)d km'%{"v1":theLaser, "v2":Pin, "v4":looplength}
                args.plt_range = [0.05, 0.82, 25, 32] if PLOT_VS_PRAT else [0.0, 4.0, 25, 32]

                Plotting.plot_multiple_curves_with_errors(hv_data, args)

                PLOT_LINESHAPES = False

                if PLOT_LINESHAPES:
                    # Plot lineshapes together
                    hv_data = []; marks = []; labs = []; 
                
                    # for i in range(0, len(Deff), 1):
                    #     thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/CNR_Meas_6_3_2025/Lineshape_NKT_T_35_I_200_VVOA_35.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[i]}
                    #     thedata = numpy.loadtxt(thefile, delimiter = '\t', unpack = False)
                    #     Ymax = numpy.max(thedata[1])
                    #     thedata[1] = thedata[1] - Ymax
                    #     hv_data.append(thedata); labs.append('D = %(v1)d km, V$_{VOA}$ = 3.5V'%{"v1":Deff[i]}); marks.append(Plotting.labs_lins[i]);
                    
                    for i in range(0, len(Deff), 1):
                        thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/CNR_Meas_6_3_2025/Lineshape_NKT_T_35_I_200_VVOA_0.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[i]}
                        thedata = numpy.loadtxt(thefile, delimiter = '\t', unpack = False)
                        Ymax = numpy.max(thedata[1])
                        thedata[1] = thedata[1] - Ymax
                        hv_data.append(thedata); labs.append('D = %(v1)d km, V$_{VOA}$ = 0V'%{"v1":Deff[i]}); marks.append(Plotting.labs_dotted[i]);

                    args = Plotting.plot_arg_multiple()
                    args.loud = True
                    args.x_label = 'Frequency' + FUnits
                    args.y_label = 'Power / dBm' + LWUNits
                    args.crv_lab_list = labs
                    args.mrk_list = marks
                    args.fig_name = '%(v1)s_CNR_Lineshapes_VVOA_0'%{"v1":theLaser}
                    args.plt_range = [-50, 50, -40, 0]

                    Plotting.plot_multiple_curves(hv_data, args)
                
                    del hv_data; del marks; del labs; 

            RESULTS_COMPAR = False
            
            if RESULTS_COMPAR: 

                Deff = [200, 400]
                theLaser = 'NKT'
                temperature = 35    
                RBW = '100Hz' # RBW used in the measurement
                FUnits = ' / kHz'
                LWUNits = ' / ' + RBW
                
                # Load the data into memory

                thedata = []
                for i in range(0, len(Deff), 1):
                    thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Loop_Power_Variation_Mar_25/Measurement_Results_I_200.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[i]}
                    if glob.glob(thefile):
                        print("Reading: ",thefile)
                        thedata.append(numpy.loadtxt(thefile, delimiter = '\t', unpack = True, skiprows = 1))

                #theerror = numpy.array([]) # instantiate an empty numpy array
                theerror = []
                for i in range(0, len(Deff), 1):
                    thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Loop_Power_Variation_Mar_25/Measurement_Errors_I_200.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[i]}
                    if glob.glob(thefile):
                        print("Reading: ",thefile)
                        theerror.append(numpy.loadtxt(thefile, delimiter = '\t', unpack = True, skiprows = 1))
                        
                # Make some plots of the data
                # make a plot of various measured values versus Power Ratio
                # col 0: P1 / dBm col 1: P2 / dBm col 2: P2 / P1 col 3: Pmax / dBm col 4: LLest / units col 5: LLVfit / units col 6: LLLfit / units col 7: LL-20 / units col 8: LLVLor / units col 9: LLVGau / units col 10: RBW / units
                # 2. P1, P2 versus Power Ratio with Errors
                # 1. Pmax versus Power Ratio with Errors
                # 3. LLest versus Power Ratio with Errors
                # 4. LL-20 versus Power Ratio with Errors
                # 5. LLVfit versus Power Ratio with Errors
                # 6. Voigt_Lor_HWHM, LLest_-20 versus Power Ratio with Errors
                # 7. Voigt_Lor_HWHM, Voigt_Gau_Stdev versus Power Ratio with Errors
                #         
                PLOT_VS_PRAT = True # Generate the plot with Power Ratio along the x-axis, other wise plot versus V_{VOA}
                RBWstr = '100Hz'
                LLMunitstr = 'kHz'
                VVOA = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
                Xvals = []
                LL_20_scale = 2.0*math.sqrt(99.0) # constant for converting LL-20 values into LL-Lorentzian values

                y_labels = ['Spectral Peak Value (dBm / %(v1)s )'%{"v1":RBWstr}, 
                            'Laser Linewidth Estimate ( %(v1)s )'%{"v1":LLMunitstr}, 
                            'Laser Linewidth at -20 dB ( %(v1)s )'%{"v1":LLMunitstr},
                            'Laser Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}, 
                            'Intrinsic Linewidth ( %(v1)s )'%{"v1":LLMunitstr}, 
                            '1/f Noise ( %(v1)s )'%{"v1":LLMunitstr}]

                fig_names = ['Spectral_Peak_Value', 
                            'Laser_Linewidth_Estimate',
                            'Laser_Linewidth_20dB',
                            'Laser_Linewidth_Voigt_Fit', 
                            'Intrinsic_Linewidth', 
                            '1_f_Noise']
                
                col_indices = [3, 4, 7, 5, 8, 9]
                
                Xvals = thedata[0][2] if PLOT_VS_PRAT else VVOA
                startVal = 0 # ignore the data at the start of the VVOA sweep? 
                endVal = numpy.size(thedata[0][2])

                for j in range(0, len(y_labels), 1):
                    
                    hv_data = []; marks = []; labels = []; 
                    
                    for i in range(0, len(Deff), 1):                                      
                        # read the data from the file
                        hv_data.append([Xvals[startVal:endVal], thedata[i][ col_indices[j] ][startVal:endVal], numpy.absolute( theerror[i][ col_indices[j] ][startVal:endVal] ) ] )
                        labels.append('D = %(v1)d (km)'%{"v1":Deff[i]})
                        marks.append(Plotting.labs[i%(len(Plotting.labs))])
                    
                    # 1. Pmax versus Power Ratio with Errors
                    args = Plotting.plot_arg_multiple()

                    args.loud = True
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                    args.y_label = y_labels[j]
                    args.fig_name = fig_names[j] + '_vs_Prat' if PLOT_VS_PRAT else fig_names[j] + '_vs_VVOA'

                    Plotting.plot_multiple_curves_with_errors(hv_data, args)

            INTERP_TEST = False
            
            if INTERP_TEST:
                Vvoa = 3.8
                Prat = Compute_Prat(Vvoa)
                print("Vvoa = ",Vvoa,", Prat = ",Prat)
                print()

                # Vvoa_data = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
                # Prat_data = [0.804, 0.805, 0.8, 0.77, 0.683, 0.519, 0.389, 0.292, 0.209, 0.111, 0.065]
                # VVOA = numpy.arange(0, 3.8, 0.2)
                # Prat_val = numpy.interp(VVOA, Vvoa_data, Prat_data)

                VVOA = numpy.arange(0, 3.8, 0.2)
                PRAT = Compute_Prat(VVOA)
                
                print(VVOA)
                print(PRAT)
                
            PLOT_SINGLE_DIST = False
            
            if PLOT_SINGLE_DIST:
                Deff = [200, 400]
                theLaser = 'NKT'
                temperature = 35    
                RBW = '100Hz' # RBW used in the measurement
                FUnits = ' / kHz'
                LWUNits = ' / ' + RBW
                
                PLOT_VS_PRAT = True
                
                # Load the data into memory
                
                # Linewidth measurement results
                indx = 1
                thedata = numpy.array([]) # instantiate an empty numpy array
                thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Loop_Power_Variation_Mar_25/Measurement_Results_I_200.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[indx]}
                if glob.glob(thefile):
                    print("Reading: ",thefile)
                    thedata = numpy.loadtxt(thefile, delimiter = '\t', unpack = True, skiprows = 1) 

                # linewidth measurement error
                theerror = numpy.array([]) # instantiate an empty numpy array
                thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/Loop_Power_Variation_Mar_25/Measurement_Errors_I_200.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[indx]}
                if glob.glob(thefile):
                    print("Reading: ",thefile)
                    theerror = numpy.loadtxt(thefile, delimiter = '\t', unpack = True, skiprows = 1)
                    
                # CNR data
                thefile = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_%(v2)s_T_%(v3)d_D_%(v4)d/CNR_Meas_6_3_2025/CNR_vs_VVOA_NKT_T_35_I_200.txt'%{"v2":theLaser, "v3":temperature, "v4":Deff[indx]}
                cnrdata = numpy.loadtxt(thefile, delimiter = '\t', unpack = True)
                #thedata[2] = 0.5*thedata[2]
                if PLOT_VS_PRAT:
                    cnrdata[0] = Compute_Prat(cnrdata[0])
                    
                # Make some plots of the data
                # make a plot of various measured values versus Power Ratio
                # col 0: P1 / dBm col 1: P2 / dBm col 2: P2 / P1 col 3: Pmax / dBm col 4: LLest / units col 5: LLVfit / units col 6: LLLfit / units col 7: LL-20 / units col 8: LLVLor / units col 9: LLVGau / units col 10: RBW / units
                # 2. P1, P2 versus Power Ratio with Errors
                # 1. Pmax versus Power Ratio with Errors
                # 3. LLest versus Power Ratio with Errors
                # 4. LL-20 versus Power Ratio with Errors
                # 5. LLVfit versus Power Ratio with Errors
                # 6. Voigt_Lor_HWHM, LLest_-20 versus Power Ratio with Errors
                # 7. Voigt_Lor_HWHM, Voigt_Gau_Stdev versus Power Ratio with Errors
                #         
                PLOT_VS_PRAT = False # Generate the plot with Power Ratio along the x-axis, other wise plot versus V_{VOA}
                RBWstr = '100Hz'
                LLMunitstr = 'kHz'
                VVOA = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
                Xvals = []
                LL_20_scale = 2.0*math.sqrt(99.0) # constant for converting LL-20 values into LL-Lorentzian values

                y_labels = ['Spectral Peak Value (dBm / %(v1)s )'%{"v1":RBWstr}, 
                            'Laser Linewidth Estimate ( %(v1)s )'%{"v1":LLMunitstr}, 
                            'Laser Linewidth at -20 dB ( %(v1)s )'%{"v1":LLMunitstr},
                            'Laser Linewidth Voigt Fit ( %(v1)s )'%{"v1":LLMunitstr}, 
                            'Intrinsic Linewidth ( %(v1)s )'%{"v1":LLMunitstr}, 
                            '1/f Noise ( %(v1)s )'%{"v1":LLMunitstr}]

                fig_names = ['Spectral_Peak_Value', 
                            'Laser_Linewidth_Estimate',
                            'Laser_Linewidth_20dB',
                            'Laser_Linewidth_Voigt_Fit', 
                            'Intrinsic_Linewidth', 
                            '1_f_Noise']
                
                col_indices = [3, 4, 7, 5, 8, 9]
                
                Xvals = thedata[2] if PLOT_VS_PRAT else VVOA
                startVal = 0 # ignore the data at the start of the VVOA sweep? 
                endVal = numpy.size(thedata[2])

                # for j in range(0, len(y_labels), 1):
                #     # 1. Pmax versus Power Ratio with Errors
                #     args = Plotting.plot_arg_multiple()

                #     args.loud = False
                #     args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                #     args.y_label = y_labels[j]
                #     args.y_label_2 = 'CNR / dB / 100Hz'
                #     args.fig_name = fig_names[j] + '_vs_Prat_D_%(v1)d'%{"v1":Deff[indx]} if PLOT_VS_PRAT else fig_names[j] + '_vs_VVOA_D_%(v1)d'%{"v1":Deff[indx]}

                #     Plotting.plot_two_y_axis(Xvals, thedata[ col_indices[j] ], cnrdata[0], cnrdata[1], args)

                # Plot the fitted lineshapes values together
                hv_data = []; labels = []; marks = []; 
                hv_data.append([ Xvals, thedata[5], theerror[5] ]); labels.append(r'$\Delta\nu_{Voigt}$'); marks.append(Plotting.labs[0])
                hv_data.append([ Xvals, thedata[8], theerror[8] ]); labels.append(r'$\Delta\nu_{white}$'); marks.append(Plotting.labs[1]); 
                hv_data.append([ Xvals, thedata[9], theerror[9] ]); labels.append(r'$\Delta\nu_{1/f}$'); marks.append(Plotting.labs[2]); 
    
                args = Plotting.plot_arg_multiple()
                args.loud = True
                args.x_label = 'Power Ratio P$_{2}$ / P$_{1}$' if PLOT_VS_PRAT else 'VOA Bias (V)'
                args.y_label = 'Laser Linewidth ( %(v1)s )'%{"v1":LLMunitstr}
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.plt_range = [0, 0.82, 0, 3.5] if PLOT_VS_PRAT else [0, 3.8, 0, 3.5]
                args.fig_name = 'Laser_Linewidth'+'_vs_Prat_D_%(v1)d'%{"v1":Deff[indx]} if PLOT_VS_PRAT else 'Laser_Linewidth'+'_vs_VVOA_D_%(v1)d'%{"v1":Deff[indx]}
                
                Plotting.plot_multiple_curves_with_errors(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Compute_Prat(Vvoa_val):
    
    # Use the known (Vvoa, Prat) values to compute new Prat values using interpolation
    # R. Sheehan 10 - 3 - 2025
    
    FUNC_NAME = ".Compute_Prat()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME 
    
    try:
        c1 = True if Vvoa_val >= 0.0 and Vvoa_val <= 4.0 else False
        
        if c1:
            Vvoa_data = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
            Prat_data = [0.804, 0.805, 0.8, 0.77, 0.683, 0.519, 0.389, 0.292, 0.209, 0.111, 0.065]
            Prat_val = numpy.interp(Vvoa_val, Vvoa_data, Prat_data)
            return Prat_val
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nCannot interpolate\nVvoa_val outside range [0, 4]\n"
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Compute_Prat(Vvoa_arr):
    
    # Use the known (Vvoa, Prat) values to compute new Prat values using interpolation
    # R. Sheehan 10 - 3 - 2025
    
    FUNC_NAME = ".Compute_Prat()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME 
    
    try:
        c1 = True if numpy.size(Vvoa_arr) > 0 else False
        c2 = True if Vvoa_arr is not None else False
        c3 = c1 and c2
        
        if c3:
            Vvoa_data = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 2.8, 3.0, 3.2, 3.5, 3.7]
            Prat_data = [0.804, 0.805, 0.8, 0.77, 0.683, 0.519, 0.389, 0.292, 0.209, 0.111, 0.065]
            Prat_arr = numpy.interp(Vvoa_arr, Vvoa_data, Prat_data)
            return Prat_arr
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nCannot interpolate\nVvoa_val outside range [0, 4]\n"
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)