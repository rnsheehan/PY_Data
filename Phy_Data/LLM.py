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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/'

        method = 'DSHI'
        laser = 'JDSU_DFB'
        temperature = '20'
        dlength = '10'

        dir_name = '%(v1)s_%(v2)s_T_%(v3)s_D_%(v4)s/'%{"v1":method, "v2":laser, "v3":temperature, "v4":dlength}

        new_dir = DATA_HOME + dir_name

        if os.path.isdir(new_dir):
            os.chdir(new_dir)

            print(os.getcwd())

            filename = glob.glob('LLM_Data_Nmeas_300*.txt')

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Sample_Data/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            nfiles = 12
            for i in range(40, 66, 5):
                #file_tmplt = 'Smpl_LLM_%(v1)d_fit_results.txt'%{"v1":i}
                file_tmplt = 'LLM_Spctrm_I_%(v1)d_fit_results.txt'%{"v1":i}
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
                    #args.plt_range = [70, 90, 0, 4]

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
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/Sample_Data/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            vals = numpy.arange(17)
            
            file_tmplt = 'Fitted_Parameter_Values.txt'
            if glob.glob(file_tmplt):
                hv_data = []; marks = []; labels = []
                data = numpy.loadtxt(file_tmplt, delimiter = ',', skiprows = 1, unpack = True, usecols = list(range(1, 12)))

                ## Peak Vals
                #hv_data.append([vals, data[0]]); labels.append('Raw PSD Peak'); marks.append(Plotting.labs_pts[0])
                #hv_data.append([vals, data[6]]); labels.append('Voigt Peak'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([vals, data[10]]); labels.append('Lorentz Peak'); marks.append(Plotting.labs_pts[2])
                #f_ending = '_peaks'

                ## HWHM Vals
                #hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([vals, data[9]]); labels.append('Lorentz HWHM'); marks.append(Plotting.labs_pts[2])
                #f_ending = '_HWHM'

                # HWHM Vals
                hv_data.append([vals, data[5]]); labels.append('Voigt HWHM'); marks.append(Plotting.labs_pts[1])
                hv_data.append([vals, data[3]]); labels.append('Voigt $\gamma$'); marks.append(Plotting.labs_pts[2])
                hv_data.append([vals, data[4]]); labels.append('Voigt $\sigma$'); marks.append(Plotting.labs_pts[3])
                f_ending = '_Voigt_vals'

                ## HWHM Vals
                #sub_data = []
                #for i in range(0, len(data[5]), 1):
                #    sub_data.append([data[5, i], data[3, i], data[4, i]])
                #Common.sort_multi_col(sub_data)

                ##hv_data.append([data[5], data[3]]); labels.append('Lorentz $\gamma$'); marks.append(Plotting.labs_pts[1])
                ##hv_data.append([data[5], data[4]]); labels.append('Gauss $\sigma$'); marks.append(Plotting.labs_pts[2])
                #hv_data.append([Common.get_col(sub_data,0), Common.get_col(sub_data,1)]); labels.append('Lorentz $\gamma$'); marks.append(Plotting.labs_pts[1])
                #hv_data.append([Common.get_col(sub_data,0), Common.get_col(sub_data,2)]); labels.append('Gauss $\sigma$'); marks.append(Plotting.labs_pts[2])
                #f_ending = '_Voigt_ctps'

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
                #args.x_label = 'Frequency / MHz'
                #args.y_label = 'Spectral Power / uW'
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


