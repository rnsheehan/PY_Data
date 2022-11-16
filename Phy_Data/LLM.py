import sys
import os 
import glob
import re

import math
import scipy
import numpy
import matplotlib.pyplot as plt

import pandas
import pprint

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
        dir_name = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/JDSU_DFB_EDFA/'

        if os.path.isdir(dir_name):
            os.chdir(dir_name)
            print(os.getcwd())

            files = glob.glob('DFB_LIV_T_*.txt')
            
            # Plot the measured LIV data            
            hv_data_v = []; hv_data_mW = []; hv_data_dBm = []; marks = []; labels = []; 
            indices = [0, 3, 5]
            for i in range(0, len(indices), 1):
                labels.append(files[ indices[i] ].replace('DFB_LIV_','').replace('.txt','').replace('_',' = '))
                marks.append( Plotting.labs_lins[ i % ( len( Plotting.labs_lins ) ) ] )
                data = numpy.loadtxt(files[ indices[i] ], delimiter = '\t', unpack = True)
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
            args.fig_name = 'JDSU_DFB_Voltage'
            args.plt_range = [0, 50, 0, 1.1]

            #Plotting.plot_multiple_curves(hv_data_v, args)

            args.y_label = '$P_{DFB}$ / mW'
            args.fig_name = 'JDSU_DFB_PmW'
            args.plt_range = [0, 50, 0, 7]

            #Plotting.plot_multiple_curves(hv_data_mW, args)

            args.y_label = '$P_{DFB}$ / dBm'
            args.fig_name = 'JDSU_DFB_PdBm'
            args.plt_range = [0, 50, -40, 10]

            #Plotting.plot_multiple_curves(hv_data_dBm, args)

            # Plot the peak voltage, power as function of temperature
            Tvals = []
            Vpeak = []
            Ppeak = []
            for i in range(0, len(files), 1):
                Tvals.append( float( files[ i ].replace('DFB_LIV_T','').replace('.txt','').replace('_','') ) )
                data = numpy.loadtxt(files[ i ], delimiter = '\t', unpack = True)
                Vpeak.append(data[1][-1])
                Ppeak.append(data[2][-1])

            # plot the data
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = '$T_{DFB}$ / C'
            args.y_label = '$V_{DFB}$ / V'
            args.y_label_2 = '$P_{DFB}$ / mW'
            args.fig_name = 'JDSU_DFB_I_50'
            
            Plotting.plot_two_axis(Tvals, Vpeak, Ppeak, args)            

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            Vvals = ['000','100','200','300','325','350','360','365','370','375','400']
            Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]

            filetmplt = 'JDSU_DFB_T_20_I_50_V_%(v1)s_fit_results.txt'

            nfiles = 12
            for i in range(0, len(Vvals), 1):
                #file_tmplt = 'Smpl_LLM_%(v1)d_fit_results.txt'%{"v1":i}
                #file_tmplt = 'LLM_Spctrm_I_%(v1)d_fit_results.txt'%{"v1":i}
                file_tmplt = filetmplt%{"v1":Vvals[i]}
                if glob.glob(file_tmplt):
                    hv_data = []; marks = []; labels = []
                    data = numpy.loadtxt(file_tmplt, delimiter = ',')
                    hv_data.append([data[0], data[1]]); labels.append('Raw PSD'); marks.append(Plotting.labs_lins[0])
                    hv_data.append([data[0], data[2]]); labels.append('Voigt'); marks.append(Plotting.labs_lins[1])
                    hv_data.append([data[0], data[4]]); labels.append('Lorentz'); marks.append(Plotting.labs_lins[2])

                    # make the plot
                    args = Plotting.plot_arg_multiple()

                    args.loud = False
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'Frequency / MHz'
                    args.y_label = 'Spectral Power / uW'
                    args.fig_name = file_tmplt.replace('.txt','')
                    args.plt_range = [60, 100, 0, 0.1]

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            Vvals = ['000','100','200','300','325','350','360','365','370','375','400']
            Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]

            #vals = numpy.arange(17)
            #vals = numpy.arange(11)
            vals = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]
            
            file_tmplt = 'Fitted_Parameter_Values.txt'
            if glob.glob(file_tmplt):
                hv_data = []; marks = []; labels = []
                data = numpy.loadtxt(file_tmplt, delimiter = ',', skiprows = 1, unpack = True, usecols = list(range(1, 12)))

                ## Peak Vals
                #hv_data.append([vals, data[0]]); labels.append('Raw PSD Peak'); marks.append(Plotting.labs_pts[0])
                #hv_data.append([vals, data[6]]); labels.append('Voigt Peak'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([vals, data[10]]); labels.append('Lorentz Peak'); marks.append(Plotting.labs_pts[2])
                #f_ending = '_peaks'
                #y_lab = 'PSD Peak Values / uW'
                #x_lab = 'VOA Bias / V'

                ## HWHM Vals
                #hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([vals, data[9]]); labels.append('Lorentz HWHM'); marks.append(Plotting.labs_pts[2])
                #f_ending = '_HWHM'
                #y_lab = 'Fitted HWHM / MHz'
                #x_lab = 'VOA Bias / V'

                # HWHM Vals
                hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                hv_data.append([vals, data[3]]); labels.append('Voigt $\gamma$'); marks.append(Plotting.labs_pts[2])
                hv_data.append([vals, data[4]]); labels.append('Voigt $\sigma$'); marks.append(Plotting.labs_pts[3])
                f_ending = '_Voigt_vals'
                y_lab = 'Voigt Fit Parameters / MHz'
                x_lab = 'VOA Bias / V'

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
                #args.plt_range = [70, 90, 0, 4]

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
            #OEWaves_FNPSD_Multiple(filelst, laser_name, False)
            OEWaves_FNPSD_Integration(filelst, True)

            # JDSU DFB NKT FNPSD Comparison
            filelst = ['JDSU_DFB_T_20_I_50_PN_3.txt', 'NKT_T_25_I_110_PN_1.txt']
            laser_name = 'DFB_NKT'
            #OEWaves_FNPSD_Multiple(filelst, laser_name, True)
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
            
            PLOT_SINGLE = True

            Vvals = ['000','100','200','300','325','350','360','365','370','375','400']
            Vvolts = [0.0, 1.0, 2.0, 3.0, 3.25, 3.5, 3.6, 3.65, 3.7, 3.75, 4.0]

            filetmplt = 'JDSU_DFB_T_20_I_50_V_%(v1)s.txt' if PLOT_SINGLE else 'JDSU_DFB_T_20_I_50_V_%(v1)s_Full.txt'

            # Import the data
            hv_data = []
            labels = []
            marks = []
            
            for ss in range(0, len(Vvals), 1): 
                filename = filetmplt%{"v1":Vvals[ss]}
                if glob.glob(filename):
                    data = numpy.loadtxt(filename, unpack = True)
                    hv_data.append(data)
                    labels.append('V$_{VOA}$ = %(v1)0.2f V'%{"v1":Vvolts[ss]})
                    marks.append(Plotting.labs_lins[ss%len(Plotting.labs_lins)])

            BASIC_PLOT = False

            if BASIC_PLOT:
                # Plot the data
                args = Plotting.plot_arg_multiple()
                
                # Extended LL Plot
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm )'
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
                for ii in range(0, len(hv_data), 1):
                    peak_data.append( Extract_Peak_Data(hv_data[ii][0], hv_data[ii][1]) )

                # Plot the data
                args = Plotting.plot_arg_multiple()

                # Extended LL Peaks Plot
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Frequency ( MHz )'
                args.y_label = 'Spectral Power ( dBm )'
                args.plt_range = [0, 3000, -90, -55]
                args.fig_name = 'ESA_Full_Peaks'
            
                Plotting.plot_multiple_curves(peak_data, args)

                del peak_data; 

            SINGLE_ANALYSIS = True

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/ESA_Spectra_Versus_VOA_Bias/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

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

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)