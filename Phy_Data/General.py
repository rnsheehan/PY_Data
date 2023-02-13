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

def Superlum_Amplification():

    # plots relating to measurement of Superlum SLD amplification
    # R. Sheehan 30 - 1 - 2023

    FUNC_NAME = ".Superlum_Amplification()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Data/Superlum_Amplification/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Declarate your lists
            hv_data = []; labels = []; marks = [];

            # EDFA_Files
            READ_EDFA = False
            EDFA_file = glob.glob("EDFA*.txt")

            # Make a plot of the data             
            if READ_EDFA:
                labels.append('Res 1 nm')
                labels.append('Res 0.05 nm')
                for i in range(0, len(EDFA_file), 2):
                    data = numpy.loadtxt(EDFA_file[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_lins[i] )    

            # Superlum SLD
            READ_SLD = False
            READ_SLD_AMP = False
            PLOT_POW = False
            PLOT_FULL = False
            PLOT_FILT = True
            SLD_file = glob.glob("SLD*2023.txt")
            SLD_file_Amp = glob.glob("SLD*2023_Amp.txt")
            SLD_file_full = glob.glob("SLD*Full*.txt")
            #SLD_file_filt = glob.glob("SLD*_1_13*.txt")
            SLD_file_filt = ['SLD_T_125_I_400_Filtered_Santec_1_13_2_2023.txt','SLD_T_125_I_300_Filtered_Santec_1_13_2_2023.txt','SLD_T_125_I_400_UnFiltered_1_13_2_2023.txt','SLD_T_125_I_300_UnFiltered_1_13_2_2023.txt']
            #SLD_file_filt = ['SLD_T_125_I_400_Filtered_Santec_FP_Amp_1_13_2_2023.txt',
            #                 'SLD_T_125_I_400_Filtered_Santec_1_13_2_2023.txt',
            #                 'SLD_T_125_I_400_UnFiltered_1_13_2_2023.txt']
            SLD_curr = [300, 350, 400]
            SLD_pow = [6.82, 8.24, 9.23]
            SLD_pow_amp = [11.51, 11.74, 11.93]

            SLD_curr = [300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400]
            SLD_pow = [6.83, 7.15, 7.45, 7.74, 8.00, 8.25, 8.48, 8.70, 8.90, 9.09, 9.28]
            SLD_pow_filt = [-16.60, -16.23, -15.90, -15.58, -15.30, -15.03, -14.78, -14.56, -14.35, -14.14, -13.95]

            if READ_SLD:           
                for i in range(0, len(SLD_file), 1):
                    data = numpy.loadtxt(SLD_file[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_lins[i] )    
                    #labels.append('%(v1)s'%{"v1":SLD_file[i]})
                    labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})

            if READ_SLD_AMP:           
                for i in range(0, len(SLD_file_Amp), 1):
                    data = numpy.loadtxt(SLD_file_Amp[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_lins[i] )    
                    #labels.append('%(v1)s'%{"v1":SLD_file[i]})
                    labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})

                for i in range(0, len(SLD_file), 1):
                    data = numpy.loadtxt(SLD_file[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_dotdash[i] )    
                    #labels.append('%(v1)s'%{"v1":SLD_file[i]})
                    labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})

                data = numpy.loadtxt(EDFA_file[-1], delimiter = '\t', unpack = True)
                hv_data.append(data)
                marks.append( Plotting.labs_line_only[0] ) 
                labels.append('EDFA')

            if PLOT_POW:
                #hv_data.append([SLD_curr, SLD_pow]); marks.append(Plotting.labs[0]); labels.append('Not Amp')
                #hv_data.append([SLD_curr, SLD_pow_amp]); marks.append(Plotting.labs[1]); labels.append('Amp')
                hv_data.append([SLD_curr, SLD_pow]); marks.append(Plotting.labs[0]); labels.append('Unfiltered')
                hv_data.append([SLD_curr, SLD_pow_filt]); marks.append(Plotting.labs[1]); labels.append('Filtered')

            if PLOT_FULL:
                for i in range(0, len(SLD_file_full), 1):
                    data = numpy.loadtxt(SLD_file_full[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_lins[i] )    
                    #labels.append('%(v1)s'%{"v1":SLD_file[i]})
                    #labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})
                labels.append('Not Amp')
                labels.append('Amp')

                data = numpy.loadtxt(EDFA_file[-1], delimiter = '\t', unpack = True)
                hv_data.append(data)
                marks.append( Plotting.labs_line_only[0] ) 
                labels.append('EDFA')

            if PLOT_FILT: 
                for i in range(0, len(SLD_file_filt), 1):
                    data = numpy.loadtxt(SLD_file_filt[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    #marks.append( Plotting.labs_lins[i] )    
                    #labels.append('%(v1)s'%{"v1":SLD_file_filt[i]})
                    #labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})
                marks.append(Plotting.labs_lins[0])
                #marks.append(Plotting.labs_dashed[0])
                marks.append(Plotting.labs_lins[1])
                marks.append(Plotting.labs_dashed[0])
                marks.append(Plotting.labs_dashed[1])
                #labels.append('SLD-761 + OTF-320 + EDFA')
                labels.append('SLD-761 + OTF-320')
                labels.append('SLD-761 + OTF-320')
                labels.append('SLD-761 I = 400 mA')
                labels.append('SLD-761 I = 300 mA')

            # Read the files for the FBG Laser
            PLOT_FBG = False
            fbg_file = glob.glob("FBG*2023.txt")
            PLOT_FBG_Zoom = False
            fbg_file = glob.glob("FBG*2023_Zoom*.txt")
            fbg_curr = [50, 60, 70, 80, 90, 100]
            fbg_pow = [2.87, 6.19, 8.39, 9.87, 10.98, 11.52]

            if PLOT_FBG:
                # plot the FBG power
                args = Plotting.plot_arg_single()

                args.loud = True
                args.curve_label = 'T = 25 C'
                args.marker = Plotting.labs[0]
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (dBm)'
                args.fig_name = 'FBG_Power'

                Plotting.plot_single_curve(fbg_curr, fbg_pow, args)

            if PLOT_FBG:
                for i in range(0, len(fbg_file), 1):
                    data = numpy.loadtxt(fbg_file[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_lins[i] )    
                    #labels.append('%(v1)s'%{"v1":fbg_file[i]})
                    #labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})
                labels.append('I = 50 mA')
                labels.append('I = 100 mA')

            if PLOT_FBG_Zoom:
                for i in range(0, len(fbg_file), 1):
                    data = numpy.loadtxt(fbg_file[i], delimiter = '\t', unpack = True)
                    hv_data.append(data)
                    marks.append( Plotting.labs_lins[i] )    
                    #labels.append('%(v1)s'%{"v1":fbg_file[i]})
                    #labels.append('I = %(v1)d mA'%{"v1":SLD_curr[i]})
                labels.append('Meas. 1')
                labels.append('Meas. 2')

            # Make a plot to compare the PM readings from the different PM
            PM_COMPARE = False
            pm_file = glob.glob("FBG_Pump_LIV*.txt")
            print(pm_file)

            if PM_COMPARE:
                for i in range(0, len(pm_file), 1):
                    data = numpy.loadtxt(pm_file[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[2]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append(pm_file[i])

                # Plot the data obtained from the S144C PM
                args = Plotting.plot_arg_single()

                args.loud = True
                args.curve_label = 'T = 25 C'
                args.marker = Plotting.labs[0]
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (mW)'
                args.fig_name = 'FBG_Power_Full'

                Plotting.plot_single_curve(hv_data[3][0], hv_data[3][1], args)

            # Generate the plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            if READ_EDFA: 
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm)'
                args.fig_name = 'EDFA_Spectrum'
            if READ_SLD: 
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.1 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Spectrum'
            if READ_SLD_AMP: 
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Spectrum_Amp_Unamp_EDFA'
            if PLOT_POW:
                args.x_label = 'SLD Current (mA)'
                args.y_label = 'SLD Power (dBm)'
                args.fig_name = 'SLD_Power'
            if PLOT_FULL:
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.1 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Full_Spectrum_Amp_Unamp'
            if PLOT_FILT:
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Filtered_Spectrum_Unamp'
                #args.fig_name = 'SLD_Filtered_Spectrum_Amp_1'
            if PLOT_FBG:
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.5 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'FBG_Full_Spectrum'
            if PLOT_FBG_Zoom:
                args.x_label = 'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [970, 980, -50, 12]
                args.fig_name = 'FBG_Full_Spectrum_Zoom'
            if PM_COMPARE:
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (mW)'
                args.fig_name = 'PM_Comparison'

            Plotting.plot_multiple_curves(hv_data, args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find: ' + DATA_HOME + '\n'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)