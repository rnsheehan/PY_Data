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
                args.x_label = '$I_{DFB}$ / mA'
                args.y_label = '$V_{DFB}$ / V'
                args.fig_name = 'JDSU_CQF915_508_Voltage'
                #args.plt_range = [0, 50, 0, 1.1]

                Plotting.plot_multiple_curves(hv_data_v, args)

                args.y_label = '$P_{DFB}$ / mW'
                args.fig_name = 'JDSU_CQF915_508_PmW'
                #args.plt_range = [0, 50, 0, 7]

                Plotting.plot_multiple_curves(hv_data_mW, args)

                args.y_label = '$P_{DFB}$ / dBm'
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
                args.x_label = '$T_{DFB}$ / C'
                args.y_label = '$V_{DFB}$ / V'
                args.y_label_2 = '$P_{DFB}$ / mW'
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
                    args.x_label = 'Wavelength $\lambda$ / nm'
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
                    args.x_label = '$T_{DFB}$ / C'
                    args.y_label = '$\lambda_{peak}$ / nm'
                    args.y_label_2 = '$P_{peak}$ / dBm / 0.05 nm'
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
            LLstd = numpy.std(data[LL_col])
            LLspread = 0.5*(numpy.max(data[LL_col]) - numpy.min(data[LL_col]))

            # get average R^{2} + error
            Rave = numpy.mean(data[LL_col_Rsqr])
            Rstd = numpy.std(data[LL_col_Rsqr])
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
            args.y_label = '$\Delta \\nu$ / MHz'
            args.plt_title = '<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, r = %(v3)0.3f'%{"v1":LLave,"v2":LLstd, "v3":LLrcoeff[0][1]}
            args.fig_name = filename.replace('.txt','_') + 'LLMvsTime'
            #args.plt_range = [0, 60, 1, 2]

            Plotting.plot_single_linear_fit_curve(data[time_col]/60.0, data[LL_col], args)

            # Plot histogram of LLM data
            
            args.x_label = 'Laser Linewidth / MHz'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram'
            args.plt_title = '<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":LLave,"v2":LLstd, "v3":KK}

            Plotting.plot_histogram(data[LL_col], args)

            args.x_label = 'Lorentzian Fit $R^{2}$ coefficient'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram_Rsqr'
            args.plt_title = '$R^{2}$ = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":Rave,"v2":Rstd, "v3":KKR}

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
            LLstd = numpy.std(data[3])
            LLspread = 0.5*(numpy.max(data[3]) - numpy.min(data[3]))

            # get average R^{2} + error
            Rave = numpy.mean(data[5])
            Rstd = numpy.std(data[5])
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
            args.y_label = '$\Delta \\nu$ / MHz'
            args.plt_title = '<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, r = %(v3)0.3f'%{"v1":LLave,"v2":LLspread, "v3":LLrcoeff[0][1]}
            args.fig_name = filename.replace('.txt','_') + 'LLMvsTime'
            args.plt_range = [0, 60, 1, 2]

            Plotting.plot_single_linear_fit_curve(data[0]/60.0, data[3], args)

            # Plot histogram of LLM data
            
            args.x_label = 'Laser Linewidth / MHz'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram'
            args.plt_title = '<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":LLave,"v2":LLspread, "v3":KK}

            Plotting.plot_histogram(data[3], args)

            args.x_label = 'Lorentzian Fit $R^{2}$ coefficient'
            args.y_label = 'Frequency'
            args.fig_name = filename.replace('.txt','_') + 'Histogram_Rsqr'
            args.plt_title = '$R^{2}$ = %(v1)0.2f +/- %(v2)0.2f MHz, k = %(v3)0.3f'%{"v1":Rave,"v2":Rspread, "v3":KKR}

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
            args.x_label = 'Inverse Power $P^{-1}$ / mW$^{-1}$'
            args.y_label = 'Laser Linewidth $\Delta \\nu$ / MHz'
            #args.plt_title = '<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz'%{"v1":LLave,"v2":LLspread}
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
            args.x_label = 'Inverse Power $P^{-1}$ / mW$^{-1}$'
            args.y_label = 'Laser Linewidth $\Delta \\nu$ / MHz'
            #args.plt_title = '<$\Delta \\nu$> = %(v1)0.2f +/- %(v2)0.2f MHz'%{"v1":LLave,"v2":LLspread}
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
                    hv_data.append([vals, data[3]]); labels.append('Voigt $\gamma$'); marks.append(Plotting.labs_pts[2])
                    hv_data.append([vals, data[4]]); labels.append('Voigt $\sigma$'); marks.append(Plotting.labs_pts[3])
                    f_ending = '_Voigt_vals'
                    y_lab = 'Voigt Fit Parameters / kHz'
                    x_lab = 'Beat Frequency / MHz'

                ## GOF chisq values
                CHISQ = False
                if CHISQ and not VALUES:
                    hv_data.append([vals, data[0]]); labels.append('Voigt'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[4]]); labels.append('Lorentz'); marks.append(Plotting.labs_pts[2])
                    f_ending = '_Fit_Chisq'
                    y_lab = 'Model Fit $\chi^{2}$'
                    x_lab = 'Beat Frequency / MHz'

                 ## GOF chisq values
                RED_CHISQ = True
                if RED_CHISQ and not VALUES:
                    hv_data.append([vals, data[2]]); labels.append('Voigt'); marks.append(Plotting.labs_pts[1])
                    hv_data.append([vals, data[6]]); labels.append('Lorentz'); marks.append(Plotting.labs_pts[2])
                    f_ending = '_Fit_Red_Chisq'
                    y_lab = 'Model Fit Reduced $\chi^{2}$'
                    x_lab = 'Beat Frequency / MHz'

                ## HWHM Vals
                #sub_data = []
                #for i in range(0, len(data[5]), 1):
                #    sub_data.append([data[5, i], data[3, i], data[4, i]])
                #Common.sort_multi_col(sub_data)

                ##hv_data.append([data[5], data[3]]); labels.append('Lorentz $\gamma$'); marks.append(Plotting.labs_pts[1])
                ##hv_data.append([data[5], data[4]]); labels.append('Gauss $\sigma$'); marks.append(Plotting.labs_pts[2])
                #hv_data.append([Common.get_col(sub_data,0), Common.get_col(sub_data,1)]); labels.append('Lorentz $\gamma$'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([Common.get_col(sub_data,0), Common.get_col(sub_data,2)]); labels.append('Gauss $\sigma$'); marks.append(Plotting.labs_pts[2])
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
        args.x_label = '$I_{set}$ mA'
        args.y_label = '$\lambda_{meas}$ nm'
        args.plt_range = [100, 200, 1549.7, 1550.4]
        args.plt_title = '$T_{set}$ = 25 C, $\lambda_{set}$ = 1550 nm'
        args.fig_name = 'NKT_Current_Tuning_meas_WL'
       
        Ivals = numpy.arange(100,210,20)
        lam_vals = [1550.054, 1550.053, 1550.053, 1550.052, 1550.052, 1550.051]
        Plotting.plot_single_linear_fit_curve(Ivals, lam_vals, args)
        
        Ivals_files = ["W0000.txt", "W0001.txt", "W0002.txt", "W0003.txt", "W0004.txt", "W0005.txt"]
        Ivals_labels = ['$I_{set}$ = 100 mA', '$I_{set}$ = 120 mA', '$I_{set}$ = 140 mA', '$I_{set}$ = 160 mA', '$I_{set}$ = 180 mA', '$I_{set}$ = 200 mA']

        SpctrmPlt.multiple_optical_spectrum_plot(DATA_DIR, Ivals_files, Ivals_labels, [1549, 1551, -50, 10], '$T_{set}$ = 25 C, $\lambda_{set}$ = 1550 nm', 'NKT_Current_Tuning')

        lam_vals = [1549.7, 1549.8, 1549.9, 1550.0, 1550.1, 1550.2, 1550.3]
        lam_vals_meas = [1549.750, 1549.849, 1549.948, 1550.048, 1550.147, 1550.247, 1550.348]

        args.loud = True
        args.x_label = '$\lambda_{set}$ nm'
        args.y_label = '$\lambda_{meas}$ nm'
        args.plt_range = [1549.7, 1550.4, 1549.7, 1550.4]
        args.plt_title = '$T_{set}$ = 25 C, $I_{set}$ = 150 mA'
        args.fig_name = 'NKT_Wavelength_Tuning_meas_WL'

        Plotting.plot_single_linear_fit_curve(lam_vals, lam_vals_meas, args)

        Ivals_files = ["W0006.txt", "W0007.txt", "W0008.txt", "W0009.txt", "W0010.txt", "W0011.txt", "W0012.txt"]
        Ivals_labels = ['$\lambda_{set}$ = 1549.7 nm', '$\lambda_{set}$ = 1549.8 nm', '$\lambda_{set}$ = 1549.9 nm', '$\lambda_{set}$ = 1550.0 nm', '$\lambda_{set}$ = 1550.1 nm', '$\lambda_{set}$ = 1550.2 nm', '$\lambda_{set}$ = 1550.3 nm']

        SpctrmPlt.multiple_optical_spectrum_plot(DATA_DIR, Ivals_files, Ivals_labels, [1549, 1551, -50, 10], '$T_{set}$ = 25 C, $I_{set}$ = 150 mA', 'NKT_Wavelength_Tuning')

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
                instantaneous_ll = float(vals[5])/1000.0 # instantaneous LL in units of kHz
                if loud: print(vals)
                if 'N/A' in preamble[-1]:
                    extended_ll_times = [float(vals[-2]), float(vals[-4]), float(vals[-6])] # extended LL observation times in units of ms
                    extended_ll_vals = [float(vals[-3]), float(vals[-5]), float(vals[-7])]
                else:
                    extended_ll_times = [float(vals[-1]), float(vals[-3]), float(vals[-5]), float(vals[-7])] # extended LL observation times in units of ms
                    extended_ll_vals = [float(vals[-2]), float(vals[-4]), float(vals[-6]), float(vals[-8])]

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

            return [meas_type, measured_data, LL_data]
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
        ll_data = []; hv_data = []; ll_marks = []; marks = []; labels = []; 
        plt_indx = 3 # this is the indx of the column storing the FNPSD data
        count = 0
        for f in filelst:
            ret_val = Parse_OEWaves_file(f)
            if 'Phase' in ret_val[0]:
                hv_data.append([ret_val[1][0], ret_val[1][plt_indx]]); 
                ll_data.append(ret_val[2])
                ll_marks.append( Plotting.labs_pts[ count%len(Plotting.labs_pts) ] ); 
                marks.append( Plotting.labs_lins[ count%len(Plotting.labs_lins) ] ); 
                labels.append('M %(v1)d'%{"v1":count+1})
                count = count + 1

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
        #args.curve_label = 'JDSU DFB Laser'
        #args.curve_label = 'NKT Fibre Laser'
        #args.marker = Plotting.labs_lins[0]
        args.x_label = 'Observation Time ( ms )'
        args.y_label = 'Linewidth ( kHz )'
        args.fig_name = laser_name + '_FNPSD_extended_LL_err'
        args.log_x = True
        args.log_y = False            

        Plotting.plot_single_curve_with_errors(ll_data[0][0], avg_LL, err_LL, args)

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

        Plotting.plot_multiple_curves(hv_data, args)

        del ll_data; del hv_data; del marks; del labels; del ret_val; 
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OEWaves_FNPSD_Integration(filelst, loud = False):
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
                    if hv_data[i][0][j] < 1e+5 and hv_data[i][1][j] > beta_slope * hv_data[i][0][j]:
                        integral = integral + ( hv_data[i][0][j] - hv_data[i][0][j-1] ) * hv_data[i][1][j]
                print('Integral ',i,': ',integral,', HWHM: ',0.5*math.sqrt(8.0*integral))
                appr_lst.append( 0.5*math.sqrt(8.0*integral) )

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
            print('HWHM: ',avg_integral/1e+6,' +/-',delta_integral/1e+6,' MHz')
            print('HWHM: ',avg_integral/1e+3,' +/-',delta_integral/1e+3,' kHz')
            print('Rel. Error: ',rel_error)
            print('')

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/OE4000_Init/'

        if(os.path.isdir(DATA_HOME)):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #filename = 'JDSU_DFB_T_20_I_50_PN_1.txt'
            #filename = 'JDSU_DFB_T_20_I_50_RIN_2.txt'
            #filename = 'NKT_T_25_I_110_FN_1.txt'
            #filename = 'NKT_T_25_I_110_RIN_2.txt'
            #OEWaves_Analysis_Single(filename, True)

            #filenames = glob.glob("*.txt")
            #for f in filenames: OEWaves_Analysis_Single(f)

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
            OEWaves_FNPSD_Integration(filelst, True)

            # NKT FNPSD
            filelst = ['NKT_T_25_I_110_PN_1.txt', 'NKT_T_25_I_110_PN_2.txt', 'NKT_T_25_I_110_FN_1.txt', 'NKT_T_25_I_110_FN_2.txt', 'NKT_T_25_I_110_FN_3.txt']
            laser_name = 'NKT'
            #OEWaves_FNPSD_Multiple(filelst, laser_name, True)
            OEWaves_FNPSD_Integration(filelst, True)

            # JDSU DFB NKT FNPSD Comparison
            filelst = ['JDSU_DFB_T_20_I_50_PN_3.txt', 'NKT_T_25_I_110_PN_1.txt']
            laser_name = 'DFB_NKT'
            #OEWaves_FNPSD_Multiple(filelst, laser_name, True)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception

        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Shengkai_LLM_22_2_2023/ZK Jia_test results_24_2_2023/'

        if(os.path.isdir(DATA_HOME)):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #filelst = glob.glob('ZJ_Test_*_24_2_2023.txt')
            
            #filelst = ['ZJ_Test_1_24_2_2023.txt', 'ZJ_Test_2_24_2_2023.txt', 'ZJ_Test_3_24_2_2023.txt', 'ZJ_Test_4_24_2_2023.txt', 'ZJ_Test_5_24_2_2023.txt']
            #laser_name = 'ZJL_M1'
            
            filelst = ['ZJ_Test_6_24_2_2023.txt', 'ZJ_Test_7_24_2_2023.txt', 'ZJ_Test_8_24_2_2023.txt', 'ZJ_Test_9_24_2_2023.txt']
            laser_name = 'ZJL_M2'            
            
            OEWaves_FNPSD_Multiple(filelst, laser_name, True)
            
            OEWaves_FNPSD_Integration(filelst, True)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception

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
                    labels.append('$P_{2}$ = %(v1)0.2f dBm'%{"v1":powers[i]})

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
            ERR_STATEMENT = ERR_STAMENT + "Incorrect input arguments\n"
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
                hv_data.append([Vvolts, CNR15, deltaCNR15]); labels.append('$\Delta$ = 15 MHz'); marks.append(Plotting.labs_pts[0])
                hv_data.append([Vvolts, CNR20, deltaCNR20]); labels.append('$\Delta$ = 20 MHz'); marks.append(Plotting.labs_pts[1])
                hv_data.append(data); labels.append('Sweep $\Delta$ = 20 MHz'); marks.append(Plotting.labs_pts[2])

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

def Multi_LLM_Analysis():

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

    FUNC_NAME = ".Multi_LLM_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_Setup_Test/LCR_DSHI_JDSU_DFB_T_20_D_50/'
        #DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_1310/LCR_DSHI_LD5_591_T_25_D_10/'
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_NKT_T_35_D_400/'

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
            thefile = 'LLM_Data_Nmeas_200_I_300_05_04_2023_16_15.txt'

            if glob.glob(thefile):

                print("Analysing: ",thefile)

                # read the data from the file
                data = pandas.read_csv(thefile, delimiter = '\t')
                titles = list(data)

                #print(titles, ", len(titles) = ", len(titles), ", len(data) = ", data.shape[1])
                #print('')

                # Create a directory for storing the results
                resDir = thefile.replace('.txt','_Results')

                if not os.path.isdir(resDir):os.mkdir(resDir)

                os.chdir(resDir)

                # Start publilshing the results
                if not glob.glob('ResultsSummary.txt'): Multi_LLM_Fit_Params_Report(data, titles, True)

                # Perform Correlation calculations of the variables
                RUN_CORRELATIONS = True

                if RUN_CORRELATIONS:
                    # Correlations with Time
                    axis_n = 0; 
                    axes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16]
                    for axis_m in axes:
                        Multi_LLM_Correlation(data, titles, axis_n, axis_m, True, False)

                    # Correlations with Pmax
                    axis_n = 4
                    axes = [6, 7, 8, 9, 10, 14]
                    for axis_m in axes:
                        Multi_LLM_Correlation(data, titles, axis_n, axis_m, False, False)

                    # Correlations with AOM-Temperature
                    axis_n = 2
                    axes = [6, 7, 8, 9, 10, 14]
                    for axis_m in axes:
                        Multi_LLM_Correlation(data, titles, axis_n, axis_m, False, False)

                    # Correlations with LL-Est
                    axis_n = 6
                    axes = [7, 8, 9]
                    for axis_m in axes:
                        Multi_LLM_Correlation(data, titles, axis_n, axis_m, False, False)

                    # Correlation of LL-Vfit with LL-Lfit
                    axis_n = 7
                    axis_m = 8
                    Multi_LLM_Correlation(data, titles, axis_n, axis_m, False, False)

                # Make a plot of the spectra with max/min fitted params
                Multi_LLM_Extract_Fit_Params(data, titles, True)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_LLM_Correlation(dataFrame, titles, axis_n, axis_m, include_hist = True, loud = False):

    # Perform correlation analysis on two columns of the Multi-LLM data
    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
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
            KK = dataFrame[ titles[axis_m] ].kurt()
            rcoeff = dataFrame[ titles[axis_m] ].corr(dataFrame[ titles[axis_n] ])
            #LLrcoeff = numpy.corrcoef( numpy.asarray( dataFrame[ titles[axis_n] ] ), numpy.asarray( dataFrame[ titles[axis_m] ] ) ) # compute the correlation coefficient for the data pair                        

            # make a basic linear fit plot
            args = Plotting.plot_arg_single()

            # Plot the Time Series of axis_m
            args.loud = loud
            args.x_label = titles[axis_n]
            args.y_label = titles[axis_m]
            args.plt_title = '%(v1)s %(v2)0.3f +/- %(v3)0.3f, r = %(v4)0.3f'%{"v1":titles[axis_m], "v2":average, "v3":errorRange, "v4":rcoeff}
            args.fig_name = '%(v1)s_vs_%(v2)s'%{"v1":titles[axis_m].replace('/','_'), "v2":titles[axis_n].replace('/','_')}            
            Plotting.plot_single_linear_fit_curve( dataFrame[ titles[axis_n] ], dataFrame[ titles[axis_m] ], args )

            if include_hist:
                # Plot the Histogram of axis_m
                args.x_label = titles[axis_m]
                args.y_label = 'Frequency'
                args.plt_title = '%(v1)s %(v2)0.3f +/- %(v3)0.3f, K = %(v4)0.3f'%{"v1":titles[axis_m], "v2":average, "v3":errorRange, "v4":KK}
                args.fig_name = 'Histogram_%(v1)s'%{"v1":titles[axis_m].replace('/','_')}
                Plotting.plot_histogram(dataFrame[ titles[axis_m] ], args)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Multi_LLM_Extract_Fit_Params(dataFrame, titles, loud = False):

    # Extract the average of the fitted model parameters from the Multi-LLM data
    # Make a plot showing the model with the average, max, min fitted parameters
    # Use this to estimate LLM at both 3dB and 20dB levels
    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
    # Voigt = True => Plot Voigt model
    # Voigt = False => Plot Lorentz Model
    # Use C++ dll to compute model values
    # LLest = 6, LLVfit = 7, LLLfit = 8
    # Voigt params V_{h} = 10, f_{0} = 11, V_{g} = 12, V_{s} = 13
    # Lorentz params L_{h} = 14, f_{0} = 15, L_{g} = 16
    # R. Sheehan 21 - 11 - 2022

    FUNC_NAME = ".Multi_LLM_Extract_Fit_Params()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if dataFrame.empty:
            ERR_STATEMENT = ERR_STATEMENT + '\ndataFrame is empty\n'
            raise Exception
        else:
            if titles is None: titles = list(dataFrame)

            flow = -100; fhigh = 100; Nsteps = 500; 
            plt_rng = '%(v1)d %(v2)d %(v3)d'%{"v1":flow, "v2":fhigh, "v3":Nsteps}

            # Averaged Voigt Model Fit Parameters
            Vh = columnStatistics(dataFrame, titles, 10) # fitted height
            Vf0 = columnStatistics(dataFrame, titles, 11) # centre frequency
            Vgamma = columnStatistics(dataFrame, titles, 12) # Lorentzian HWHM
            Vsigma = columnStatistics(dataFrame, titles, 13) # Gaussian std. dev.

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
            Lh = columnStatistics(dataFrame, titles, 14) # fitted height
            Lf0 = columnStatistics(dataFrame, titles, 15) # centre frequency
            Lgamma = columnStatistics(dataFrame, titles, 16) # Lorentzian HWHM

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
            spctr_data = numpy.loadtxt(Lminfile, delimiter = ',', unpack = True)            
            if PLOT_IN_DBM:
                spctr_data[1] = spctr_data[1] / 1e+6 # convert uW -> mW
                spctr_data[1] = Common.list_convert_mW_dBm(spctr_data[1]) # convert mW -> dBm
            hv_data.append(spctr_data); labels.append('L$_{min}$'); marks.append(Plotting.labs_dotted[1])

            # Plot the data
            args = Plotting.plot_arg_multiple()
                
            # Extended LL Plot
            args.loud = True
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
            args.loud = True
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
            args.loud = True
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

def Multi_LLM_Fit_Params_Report(dataFrame, titles, loud = False):

    # Extract the average of the fitted model parameters from the Multi-LLM data
    # dataFrame contains the data from the Multi-LLM measurement
    # titles contains the names of the columns of data that have been measured
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
            columnStatistics(dataFrame, titles, 4, loud) # Pmax
            columnStatistics(dataFrame, titles, 6, loud) # LL estimate from data
            columnStatistics(dataFrame, titles, 7, loud) # LL from Voigt Fit
            columnStatistics(dataFrame, titles, 8, loud) # LL from Lorentz Fit
            columnStatistics(dataFrame, titles, 9, loud) # LL from Lorentz Fit
            
            print("\nVoigt Fit Parameters") # Averaged Voigt Model Fit Parameters
            columnStatistics(dataFrame, titles, 10, loud) # fitted height
            columnStatistics(dataFrame, titles, 11, loud) # centre frequency
            columnStatistics(dataFrame, titles, 12, loud) # Lorentzian HWHM
            columnStatistics(dataFrame, titles, 13, loud) # Gaussian std. dev.
            
            print("\nLorentz Fit Parameters") # Averaged Lorentz Model Fit Parameters
            columnStatistics(dataFrame, titles, 14, loud) # fitted height
            columnStatistics(dataFrame, titles, 15, loud) # centre frequency
            columnStatistics(dataFrame, titles, 16, loud) # Lorentzian HWHM
            
            print("\nAOM Temperature Statistics") # AOM Temperature Statistics
            columnStatistics(dataFrame, titles, 1, loud) # Air Temperature
            columnStatistics(dataFrame, titles, 2, loud) # AOM Temperature
            columnStatistics(dataFrame, titles, 3, loud) # AOM Driver Temperature

            sys.stdout = old_target # return to the usual stdout

            #Dict = columnStatistics(dataFrame, titles, 6, True)
            #print(Dict['Name'],':',Dict['Average'],'+/-',Dict['Err'])
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def columnStatistics(dataFrame, titles, axisNo, loud = False):

    # extract the basic statistics from a given column / axis of data
    # dataFrame is the dataset being analysed
    # titles is the list of names of the items in the dataFrame
    # axisNo is the index of the column of data being analysed
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
                stdev = dataFrame[titles[axisNo]].std()
                maxval = dataFrame[titles[axisNo]].max()
                minval = dataFrame[titles[axisNo]].min()
                errorRange = 0.5*( math.fabs(maxval) - math.fabs(minval) )
                relErr = 100*(errorRange/average)

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

    FUNC_NAME = ".Compute_Spectrum()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        V_dir = 'C:/Users/robertsheehan/Programming/C++/Fitting/Voigt/x64/Release/'
        V_exe = 'Voigt.exe '

        L_dir = 'C:/Users/robertsheehan/Programming/C++/Fitting/Lorentz/x64/Release/'
        L_exe = 'Lorentz.exe '

        DIR = V_dir if spctr_choice else L_dir
        EXE = V_exe if spctr_choice else L_exe

        args = DIR + EXE + arg_vals

        output = subprocess.call(args, stdin=None, stdout=None, stderr=None, shell=False)

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/LCR_DSHI_Setup_Test/LCR_DSHI_JDSU_DFB_T_20_D_50/Beat_3/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            f_AOM = 80
            loop_length = 50
            f_cutoff = 720; 

            beatfiles = glob.glob('Beat_Data_Nmeas_*_I_*.txt')

            Nbeats, Titles, averaged_data, max_data, min_data = Average_Data_From_Beat_Files(beatfiles)
            
            Beat_Data_Report(Nbeats, f_AOM, loop_length, f_cutoff, Titles, averaged_data, max_data, min_data)

            Full = False
            Cutoff = True
            Loud = False
            Plot_Beat_Data(Nbeats, f_AOM, loop_length, f_cutoff, Titles, averaged_data, max_data, min_data, Full, Cutoff, Loud)                        
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Extract_Data_From_Beat_File(beatfile, loud = False):

    # Extract the data from a single beat measurement file
    # return a list with data stored as elements of the list
    # R. Sheehan 13 - 12 - 2022

    FUNC_NAME = ".Extract_Data_From_Beat_File()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(beatfile):
            # read the data from the file
            df = pandas.read_csv(beatfile, delimiter = '\t')
            titles = list(df)
            Nbeats = df.shape[0]

            dfaxes = numpy.arange(4, 19, 1)
            dfaxes = numpy.delete(dfaxes, [9, 13]) # not interested in Voigt fc (axis 9) or Lorentz fc (axis 13)

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

    # look into multiple beat files
    # extract the data from each file
    # average the data obtained from each file
    # return the data as single array
    # R. Sheehan 13 - 12 - 2022

    # Some notes on copy
    # https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment

    FUNC_NAME = ".Average_Data_From_Beat_Files()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:

        if beatfiles is not None:
            # sum the data from each file
            ave_data = []; max_data = []; min_data = [];
            sub_titles = []; Nbeats_max = -1000; Nfiles = float(len(beatfiles)); 
            for i in range(0, len(beatfiles), 1):
                Nbeats, sub_titles, data = Extract_Data_From_Beat_File(beatfiles[i], False)                
                if Nbeats > Nbeats_max:Nbeats_max = Nbeats

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

                #print(data[5][0], ',', ave_data[5][0], ',', max_data[5][0], ',', min_data[5][0])

            # Average the data obtained from all the files
            # Divde the sum over all the data by the number of Files
            for k in range(0, len(ave_data), 1):
                ave_data[k] = ave_data[k] / Nfiles

            #print(data[5][0], ',', ave_data[5][0], ',', max_data[5][0], ',', min_data[5][0])

            return [Nbeats_max, sub_titles, ave_data, max_data, min_data] 
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_Beat_Data(Nbeats, F_AOM, Loop_Length, F_CUTOFF, Titles, Average, Max, Min, Full_Plots, Cutoff_Plots, loud = False):

    # plot the averaged data with error bars
    # R. Sheehan 13 - 12 - 2022

    FUNC_NAME = ".Plot_Beat_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if Nbeats > 0 else False
        c2 = True if len(Average) > 0 else False
        #c3 = True if len(Error) > 0 else False
        # must add more conditions here

        if c1 and c2:
            fbeats = numpy.arange(F_AOM, Nbeats*F_AOM + 1, F_AOM)
            distance = numpy.arange(Loop_Length, Nbeats*Loop_Length + 1, Loop_Length )
            fend_indx = 1 + numpy.where(fbeats == F_CUTOFF)[0][0]

            if Full_Plots:
                PLOT_WITH_BEATS = True

                xvals = fbeats if PLOT_WITH_BEATS else distance
                xlabel = 'Beat Frequency / MHz' if PLOT_WITH_BEATS else 'Loop Length / km'

                labels = ['Max', 'Avg', 'Min']
                marks = [Plotting.labs_dotdash[0], Plotting.labs_lins[0], Plotting.labs_dotted[0]]

                for i in range(0, len(Average), 1):
                    hv_data = []
                    hv_data.append([xvals, Max[i]]); 
                    hv_data.append([xvals, Average[i]]); 
                    hv_data.append([xvals, Min[i]]); 

                    args = Plotting.plot_arg_multiple()                

                    args.loud = loud
                    args.x_label = xlabel
                    args.y_label = Titles[i]
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.fig_name = Titles[i].replace('/','_')
                
                    Plotting.plot_multiple_curves(hv_data, args)

                    del hv_data

            if Cutoff_Plots:
                PLOT_WITH_BEATS = True

                xvals = fbeats if PLOT_WITH_BEATS else distance
                xlabel = 'Beat Frequency / MHz' if PLOT_WITH_BEATS else 'Loop Length / km'

                labels = ['Max', 'Avg', 'Min']
                marks = [Plotting.labs_dotdash[0], Plotting.labs_lins[0], Plotting.labs_dotted[0]]

                for i in range(0, len(Average), 1):
                    Error = 0.5*(Max[i] - Min[i])
                    avg_val = numpy.mean(Average[i][0:fend_indx])
                    avg_error = numpy.mean(Error[0:fend_indx])

                    args = Plotting.plot_arg_single()                

                    args.loud = loud
                    args.x_label = xlabel
                    args.y_label = Titles[i]
                    #args.crv_lab_list = labels
                    #args.mrk_list = marks
                    args.fig_name = Titles[i].replace('/','_') + '_Err'
                    args.plt_title = "Avg = %(v1)0.3f +/- %(v2)0.3f"%{"v1":avg_val, "v2":avg_error}
                
                    Plotting.plot_single_linear_fit_curve_with_errors(xvals[0:fend_indx], Average[i][0:fend_indx], Error[0:fend_indx], args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot open ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Beat_Data_Report(Nbeats, F_AOM, Loop_Length, F_CUTOFF, Titles, Average, Max, Min):

    # Print a report on the averaged beat data values
    # R. Sheehan 15 - 12 - 2022

    FUNC_NAME = ".Beat_Data_Report()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if Nbeats > 0 else False
        c2 = True if len(Average) > 0 else False
        #c3 = True if len(Error) > 0 else False
        # must add more conditions here

        if c1 and c2:

            fbeats = numpy.arange(F_AOM, Nbeats*F_AOM + 1, F_AOM)
            fend_indx = 1 + numpy.where(fbeats == F_CUTOFF)[0][0]

            # Redirect the output to a file
            old_target, sys.stdout = sys.stdout, open('ResultsSummary.txt', 'w')

            print("System Settings")
            print("Loop length:",Loop_Length,"km")
            print("f_{AOM}:",F_AOM,"MHz")
            print("Nbeats Sampled:",Nbeats)
            print("Nbeats Useful:",fend_indx)
            print("f_{cuttoff}:",F_CUTOFF,"MHz")
            print("Effective Loop Length:",fend_indx*Loop_Length,"km")            

            print("\nResults")
            for i in range(0, len(Average), 1):
                Error = 0.5*(Max[i] - Min[i])
                avg_val = numpy.mean(Average[i][0:fend_indx])
                avg_error = numpy.mean(Error[0:fend_indx])
                #print(Titles[i],":",avg_val,"+/-",avg_error)                
                print("%(v1)s: %(v2)0.3f +/- %(v3)0.3f"%{"v1":Titles[i], "v2":avg_val, "v3":avg_error})

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