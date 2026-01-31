from genericpath import isdir
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

import pandas
import pprint

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
                    labels.append(r'$R_{s}$  = %(v2)d $\Omega$'%{"v2":int(r)})
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

    # size_diff = -3
    # print(numpy.zeros( abs(size_diff)  ))
    # print(numpy.repeat( -1000, abs(size_diff)  ))
    
    # Attempt to select a dictionary element other than the one named
    Write_Chnnls = {"A0":0, "A1":1}
    the_channel = 'A1'
    
    if the_channel == 'A0':
        print('Writing from A1:',Write_Chnnls['A1'])
    else:
        print('Writing from A0:',Write_Chnnls['A0'])

    # loop over sub indices of an array
    no_meas = 120
    no_smpls = 5000
    for j in range(0, 120, 1):
        start = j*no_smpls
        end = start + no_smpls
        print(start," to ",end)
    

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
            PLOT_POW_SINGLE = False
            PLOT_FULL = False
            PLOT_FILT = False
            SLD_file = ['SLD_T_125_I_300_26_1_2023.txt', 'SLD_T_125_I_350_26_1_2023.txt', 'SLD_T_125_I_400_26_1_2023.txt']
            SLD_file_Amp = glob.glob("SLD*2023_Amp.txt")
            SLD_file_full = glob.glob("SLD*Full*.txt")
            #SLD_file_filt = glob.glob("SLD*_1_13*.txt")
            SLD_file_filt = ['SLD_T_125_I_400_Filtered_Santec_1_13_2_2023.txt',
                             'SLD_T_125_I_300_Filtered_Santec_1_13_2_2023.txt',
                             'SLD_T_125_I_400_UnFiltered_1_13_2_2023.txt',
                             'SLD_T_125_I_300_UnFiltered_1_13_2_2023.txt']
            #SLD_file_filt = ['SLD_T_125_I_400_Filtered_Santec_FP_Amp_1_13_2_2023.txt',
            #                 'SLD_T_125_I_400_Filtered_Santec_1_13_2_2023.txt',
            #                 'SLD_T_125_I_400_UnFiltered_1_13_2_2023.txt']
            SLD_curr = [300, 350, 400]
            SLD_pow = [6.82, 8.24, 9.23]
            SLD_pow_amp = [11.51, 11.74, 11.93]

            #SLD_curr = [300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400]
            #SLD_pow = [6.83, 7.15, 7.45, 7.74, 8.00, 8.25, 8.48, 8.70, 8.90, 9.09, 9.28]
            #SLD_pow_filt = [-16.60, -16.23, -15.90, -15.58, -15.30, -15.03, -14.78, -14.56, -14.35, -14.14, -13.95]

            if PLOT_POW_SINGLE:
                # plot the SLD power
                args = Plotting.plot_arg_single()

                args.loud = True
                args.curve_label = 'T = 20 C'
                args.marker = Plotting.labs[0]
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (dBm)'
                args.fig_name = 'SLD_Only_Power'

                Plotting.plot_single_curve(SLD_curr, SLD_pow, args)

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

            # EDFA Pump Output
            PLOT_Pump = False
            PLOT_Cbnd_Pow = False
            pump_files = ['FBG_Pump_LIV_S144C_3.txt', 'CBand_EDFA_Pump_Output_No_Input_WL_980.txt']
            cbnd_pow_files = ['FBG_Pump_LIV_S144C_3.txt','CBand_EDFA_Pump_Output_No_Input_WL_1550.txt','CBand_EDFA_Amp_Output_SLD_Input_WL_1550_1.txt','CBand_EDFA_Amp_Output_SLD_Input_WL_1550_2.txt']

            if PLOT_Pump:
                for i in range(0, len(pump_files), 1):
                    data = numpy.loadtxt(pump_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[3]])
                    marks.append( Plotting.labs_lins[i] )
                    #labels.append(pump_files[i])

                labels.append('FBG Pump')
                labels.append('C-bnd No input')
                #labels.append('C-bnd 1550 nm No input')
                #labels.append('C-bnd 1550 nm SLD input')

            if PLOT_Cbnd_Pow:
                for i in range(0, len(cbnd_pow_files)-1, 1):
                    data = numpy.loadtxt(cbnd_pow_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[2]])
                    marks.append( Plotting.labs_lins[i] )
                    #labels.append(cbnd_pow_files[i])

                #labels.append('FBG Pump')
                #labels.append('C-bnd No input')
                labels.append('FBG Pump')
                labels.append('C-bnd No input')
                labels.append('C-bnd SLD input')

            # EDFA Gain Spectra
            PLOT_Cbnd_Gain = False
            PLOT_Lbnd_Gain = False
            PLOT_Gain_Compar = False
            PLOT_Gain_Compar_Short = False
            PLOT_Gain_Filt = False
            Ipump = numpy.arange(100, 401, 100)
            #Ipump = [100, 200, 300, 400]
            Cbnd_gain_files = glob.glob('Fibre_CBand_EDFA_Gain_Pump_*_15_2_2025.txt')
            Lbnd_gain_files = glob.glob('Fibre_LBand_EDFA_Gain_Pump_*_15_2_2025.txt')
            FP_file = 'EDFA_3_26_1_2023.txt'
            amp_file = 'SLD_T_125_I_400_Filtered_Santec_FP_Amp_15_2_2023.txt'
            unamp_file = 'SLD_T_125_I_400_UnFiltered_1_15_2_2023.txt'
            Full_gain_files = ['Fibre_CBand_EDFA_Gain_Pump_400_Full_15_2_2025.txt', 'Fibre_LBand_EDFA_Gain_Pump_400_Full_15_2_2025.txt','EDFA_1_26_1_2023.txt']
            JDSU_Short_gain = 'JDSU_OEM_A_I_400_ASE_20_2_2023.txt'

            if PLOT_Cbnd_Gain:
                for i in range(0, len(Cbnd_gain_files)-1, 1):
                    data = numpy.loadtxt(Cbnd_gain_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('I$_{pump}$ = %(v1)d (mA)'%{ "v1":Ipump[i] } )
                
                data = numpy.loadtxt(FP_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_line_only[1] )
                labels.append('EDFA-C-26G-S')

            if PLOT_Lbnd_Gain:
                for i in range(0, len(Lbnd_gain_files)-1, 1):
                    data = numpy.loadtxt(Lbnd_gain_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('I$_{pump}$ = %(v1)d (mA)'%{ "v1":Ipump[i] } )

                data = numpy.loadtxt(FP_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_line_only[1] )
                labels.append('EDFA-C-26G-S')

            if PLOT_Gain_Compar:
                for i in range(0, len(Full_gain_files), 1):
                    data = numpy.loadtxt(Full_gain_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )

                labels.append('C-Band')
                labels.append('L-Band')
                labels.append('EDFA-C-26G-S')

            if PLOT_Gain_Compar_Short:
                data = numpy.loadtxt(JDSU_Short_gain, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[3] )
                labels.append('JDSU OAM A')
                
                data = numpy.loadtxt(Cbnd_gain_files[-2], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[0] )
                labels.append('C-Band')

                data = numpy.loadtxt(Lbnd_gain_files[-2], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[1] )
                labels.append('L-Band')

                data = numpy.loadtxt(FP_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_line_only[1] )
                labels.append('EDFA-C-26G-S')

            if PLOT_Gain_Filt:
                data = numpy.loadtxt(JDSU_Short_gain, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[3] )
                labels.append('JDSU OAM A')

                data = numpy.loadtxt(Cbnd_gain_files[-2], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[0] )
                labels.append('C-Band')

                data = numpy.loadtxt(Lbnd_gain_files[-2], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[1] )
                labels.append('L-Band')

                data = numpy.loadtxt(FP_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_line_only[1] )
                labels.append('EDFA-C-26G-S')

                data = numpy.loadtxt(amp_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_lins[2] )
                labels.append('A1 Output')

                data = numpy.loadtxt(unamp_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_dashed[2] )
                labels.append('Filter Output')

            # Amplified Spectra
            PLOT_Config1 = False
            PLOT_Config_Combo = False
            PLOT_Config_Res = False
            Config1_files = glob.glob('SLD_T_125_I_400_Filtered_Santec_Cbnd_Amp_Pump_*_15_2_2023.txt'); CN = 1; # config-1
            Config2_files = glob.glob('SLD_T_125_I_400_Filtered_Santec_Lbnd_Amp_Pump_*_15_2_2023.txt'); CN = 2; #config-2
            Config3_files = glob.glob('SLD_T_125_I_400_Lbnd_Amp_Pump_*_Filtered_Santec_15_2_2023.txt'); CN = 3; #config-3
            Config4_files = glob.glob('SLD_T_125_I_400_Filtered_Santec_Lbnd_FP_Amp_Pump_*_15_2_2023.txt'); CN = 4; #config-4
            Config5_files = glob.glob('SLD_T_125_I_400_Filtered_Santec_FP_Lbnd_Amp_Pump_*_15_2_2023.txt'); CN = 5; #config-5
            unamp_file = 'SLD_T_125_I_400_UnFiltered_1_15_2_2023.txt'
            unfilt_file = 'SLD_T_125_I_400_UnFiltered_1_13_2_2023.txt'
            amp_file = 'SLD_T_125_I_400_Filtered_Santec_FP_Amp_15_2_2023.txt'
            final_configs = [Config1_files[-1], Config2_files[-1], Config3_files[-1], Config4_files[-1], Config5_files[-1]]
            print(Config1_files)

            if PLOT_Config1:
                for i in range(0, len(Config1_files), 1):
                    data = numpy.loadtxt(Config1_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('I$_{pump}$ = %(v1)d (mA)'%{ "v1":Ipump[i] } )

                if CN == 5:
                    data = numpy.loadtxt(amp_file, delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_line_only[2] )
                    labels.append('SLD + OTF-320 + FP')

                data = numpy.loadtxt(unamp_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_line_only[1] )
                labels.append('SLD + OTF-320')

            if PLOT_Config_Combo:

                for i in range(0, len(final_configs), 1):
                    data = numpy.loadtxt(final_configs[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('Config. = %(v1)d'%{ "v1":i+1 } )                

                data = numpy.loadtxt(unamp_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                marks.append( Plotting.labs_line_only[1] )
                labels.append('SLD + OTF-320')

            if PLOT_Config_Res:

                data = numpy.loadtxt(final_configs[-1], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                #marks.append( Plotting.labs_line_only[0] )
                marks.append( Plotting.labs_lins[3] )
                #labels.append('SLD + OTF-320 + FP + L-bnd')
                labels.append('SLD + F + A1 + A2')

                data = numpy.loadtxt(amp_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                #marks.append( Plotting.labs_line_only[2] )
                marks.append( Plotting.labs_lins[2] )
                #labels.append('SLD + OTF-320 + FP')
                labels.append('SLD + F + A1')

                data = numpy.loadtxt(unamp_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                #marks.append( Plotting.labs_line_only[1] )
                marks.append( Plotting.labs_lins[1] )
                #labels.append('SLD + OTF-320')
                labels.append('SLD + F')

                data = numpy.loadtxt(unfilt_file, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                #marks.append( Plotting.labs_line_only[1] )
                marks.append( Plotting.labs_lins[0] )
                labels.append('SLD')

            # Plot the tuned spectra
            PLOT_Tuning = False
            Band = 'C'
            WL = numpy.arange(1540, 1556, 5)
            tuned_files = glob.glob('SLD_T_125_I_400_Filtered_Santec_FP_%(v1)sbnd_Amp_Pump_400_17_2_2023_l_*.txt'%{"v1":Band})

            if PLOT_Tuning:

                for i in range(0, len(tuned_files), 1):
                    data = numpy.loadtxt(tuned_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('%(v1)d (nm)'%{ "v1":WL[i] } )

            # Plot the data related to the JDSU OAM
            PLOT_OAM_Spctr_Full = False
            PLOT_OAM_Spctr_Short = False
            PLOT_OAM_IV = False
            PLOT_OAM_AMP = True
            OAM = 'A'
            full_spctr = glob.glob('JDSU_OEM_%(v1)s_I_*_ASE_20_2_2023.txt'%{"v1":OAM})
            short_spctr = glob.glob('JDSU_OEM_%(v1)s_I_*_ASE_Short_20_2_2023.txt'%{"v1":OAM})
            OAM_IV = glob.glob('JDSU_OEM_*_IV.txt')
            OAM_AMP_files = ['SLD_T_125_I_400_Filtered_Santec_20_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_FP_Amp_20_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_FP_Cbnd_Amp_Pump_400_20_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_JDSU_A_Amp_20_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_JDSU_A_Cbnd_Amp_Pump_400_20_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_Cbnd_Amp_Pump_400_20_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_Cbnd_Amp_Pump_400_JDSU_A_20_2_2023.txt']
            STEP = 0
            Ipump = numpy.arange(100, 501, 100)

            if PLOT_OAM_Spctr_Full:
                for i in range(0, len(full_spctr), 1):
                    data = numpy.loadtxt(full_spctr[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('I$_{drv}$ = %(v1)d (mA)'%{ "v1":Ipump[i] } )

            if PLOT_OAM_Spctr_Short:
                for i in range(0, len(short_spctr), 1):
                    data = numpy.loadtxt(short_spctr[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    labels.append('I$_{drv}$ = %(v1)d (mA)'%{ "v1":Ipump[i] } )

            if PLOT_OAM_IV:
                for i in range(0, len(OAM_IV), 1):
                    data = numpy.loadtxt(OAM_IV[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])
                    marks.append( Plotting.labs_lins[i] )
                    #labels.append('I$_{drv}$ = %(v1)d (mA)'%{ "v1":Ipump[i] } )

                labels.append('OAM A')
                labels.append('OAM B')

            if PLOT_OAM_AMP:
                #STEP = 1
                #data = numpy.loadtxt(OAM_AMP_files[2], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + FP + C-band'); marks.append( Plotting.labs_lins[1] );

                #data = numpy.loadtxt(OAM_AMP_files[1], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + FP'); marks.append( Plotting.labs_lins[0] );

                STEP = 22
                data = numpy.loadtxt(OAM_AMP_files[3], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                labels.append('SLD + OTF + OAM-A'); marks.append( Plotting.labs_lins[2] );

                #data = numpy.loadtxt(OAM_AMP_files[2], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + FP + C-band'); marks.append( Plotting.labs_lins[1] );

                #STEP = 3
                #data = numpy.loadtxt(OAM_AMP_files[4], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + OAM-A + C-band'); marks.append( Plotting.labs_lins[3] );

                #data = numpy.loadtxt(OAM_AMP_files[3], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + OAM-A'); marks.append( Plotting.labs_lins[2] );

                #STEP = 4
                #data = numpy.loadtxt(OAM_AMP_files[6], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + C-band + OAM-A'); marks.append( Plotting.labs_lins[5] );

                #data = numpy.loadtxt(OAM_AMP_files[5], delimiter = '\t', unpack = True)
                #hv_data.append([data[0], data[1]])
                #labels.append('SLD + OTF + C-band'); marks.append( Plotting.labs_lins[4] );                

                data = numpy.loadtxt(OAM_AMP_files[0], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                labels.append('SLD + OTF'); marks.append( Plotting.labs_lins[1] );

                data = numpy.loadtxt('SLD_T_125_I_400_UnFiltered_1_13_2_2023.txt', delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                labels.append('SLD'); marks.append( Plotting.labs_lins[0] );
                
            # Counter Propagation Experiment
            PLOT_COUNT = False
            counter_files = ['SLD_T_125_I_400_Filtered_Santec_FP_Lbnd_Amp_Counter_Pump_400_21_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_FP_Lbnd_Amp_Pump_400_21_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_FP_Amp_21_2_2023.txt',
                             'SLD_T_125_I_400_Filtered_Santec_21_2_2023.txt']

            if PLOT_COUNT:
                for i in range(0, len(counter_files), 1):
                    data = numpy.loadtxt(counter_files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])                    

                labels.append('SLD + OTF + FP + Lcntr'); marks.append( Plotting.labs_lins[0] );
                labels.append('SLD + OTF + FP + L'); marks.append( Plotting.labs_lins[1] );
                labels.append('SLD + OTF + FP'); marks.append( Plotting.labs_lins[2] );
                labels.append('SLD + OTF'); marks.append( Plotting.labs_line_only[1] );

            # C-band EDFA altered ASE
            PLOT_Alt_ASE = False
            ASE_Files = ['JDSU_OEM_A_I_400_ASE_21_2_2023.txt',
                         'JDSU_OEM_A_I_400_ASE_20_2_2023.txt',
                         'Fibre_CBand_EDFA_Gain_Pump_400_21_2_2023.txt',
                         'Fibre_CBand_EDFA_Gain_Pump_400_15_2_2025.txt',
                         'Fibre_LBand_EDFA_Gain_Pump_400_21_2_2023.txt',
                         'Fibre_LBand_EDFA_Gain_Pump_400_15_2_2025.txt',
                         'EDFA_3_26_1_2023.txt']

            if PLOT_Alt_ASE:
                for i in range(0, len(ASE_Files), 1):
                    data = numpy.loadtxt(ASE_Files[i], delimiter = '\t', unpack = True)
                    hv_data.append([data[0], data[1]])

                labels.append('JDSU OAM-A 21-2-2023'); marks.append( Plotting.labs_lins[3] );
                labels.append('JDSU OAM-A 20-2-2023'); marks.append( Plotting.labs_dashed[3] );
                labels.append('C-band 21-2-2023'); marks.append( Plotting.labs_lins[0] );
                labels.append('C-band 15-2-2023'); marks.append( Plotting.labs_dashed[0] );
                labels.append('L-band 21-2-2023'); marks.append( Plotting.labs_lins[1] );
                labels.append('L-band 15-2-2023'); marks.append( Plotting.labs_dashed[1] );
                labels.append('EDFA-C-26G-S'); marks.append( Plotting.labs_line_only[1] );

            # Generate the plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            if READ_EDFA: 
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm)'
                args.fig_name = 'EDFA_Spectrum'
            if READ_SLD: 
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.1 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Spectrum'
            if READ_SLD_AMP: 
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Spectrum_Amp_Unamp_EDFA'
            if PLOT_POW:
                args.x_label = 'SLD Current (mA)'
                args.y_label = 'SLD Power (dBm)'
                args.fig_name = 'SLD_Power'
            if PLOT_FULL:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.1 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Full_Spectrum_Amp_Unamp'
            if PLOT_FILT:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'SLD_Filtered_Spectrum_Unamp'
                #args.fig_name = 'SLD_Filtered_Spectrum_Amp_1'
            if PLOT_FBG:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.5 nm)'
                #args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'FBG_Full_Spectrum'
            if PLOT_FBG_Zoom:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [970, 980, -50, 12]
                args.fig_name = 'FBG_Full_Spectrum_Zoom'
            if PM_COMPARE:
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (mW)'
                args.fig_name = 'PM_Comparison'
            if PLOT_Pump:
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (dBm)'
                args.fig_name = 'Pump_Power'
            if PLOT_Cbnd_Pow:
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (mW)'
                args.plt_range = [0, 300, 0, 15]
                args.fig_name = 'Cbnd_Power_mW'
            if PLOT_Cbnd_Gain:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'Cbnd_EDFA_Spectra'
            if PLOT_Lbnd_Gain:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1530, 1560, -65, -15]
                args.fig_name = 'Lbnd_EDFA_Spectra'
            if PLOT_Gain_Compar:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.1 nm)'
                args.plt_range = [1500, 1620, -65, -15]
                args.fig_name = 'EDFA_Gain_Spectra'
            if PLOT_Gain_Compar_Short:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1530, 1560, -60, 0]
                args.fig_name = 'Gain_Spectra_Compar_2'
            if PLOT_Config1:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1545, 1555, -60, 10]
                args.fig_name = 'Spectrum_Config_%(v1)d'%{"v1":CN}
            if PLOT_Config_Combo:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1545, 1555, -60, 10]
                args.fig_name = 'Combined_Config'
            if PLOT_Config_Res:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1545, 1555, -60, 10]
                args.fig_name = 'SLD_Amp_Result'
            if PLOT_Tuning:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1535, 1560, -30, 5]
                args.fig_name = 'SLD_Amp_Tuning_%(v1)sBand'%{"v1":Band}
            if PLOT_Gain_Filt: 
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1540, 1560, -60, 0]
                args.fig_name = 'Gain_Spectra_Compar_Filt_2'
            if PLOT_OAM_Spctr_Full:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.1 nm)'
                args.plt_range = [1500, 1600, -50, 0]
                args.fig_name = 'JDSU_OAM_%(v1)s_Full'%{"v1":OAM}
            if PLOT_OAM_Spctr_Short:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1540, 1560, -60, -10]
                args.fig_name = 'JDSU_OAM_%(v1)s_Short'%{"v1":OAM}
            if PLOT_OAM_IV:
                args.x_label = 'Current / mA'
                args.y_label = 'Voltage / V'
                args.plt_range = [0, 100, 0, 1.6]
                args.fig_name = 'OAM_IV_Curves_2'
            if PLOT_OAM_AMP:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1540, 1560, -60, 10]
                args.fig_name = 'JDSU_OAM_Test_%(v1)d'%{"v1":STEP}
            if PLOT_COUNT:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1540, 1560, -60, 10]
                args.fig_name = 'Counter_Prop_Test'
            if PLOT_Alt_ASE:
                args.x_label = r'Wavelength $\lambda$ (nm)'
                args.y_label = 'Power (dBm / 0.05 nm)'
                args.plt_range = [1540, 1560, -60, -10]
                args.fig_name = 'ASE_Change'

            Plotting.plot_multiple_curves(hv_data, args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot find: ' + DATA_HOME + '\n'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def PDA10CS_Calibration_3():

    # Calibration of two units of PDA10CS for use in the LCR-DSHI measurement setup
    # R. Sheehan 22 - 5 - 2023

    FUNC_NAME = ".PDA10CS_Calibration_3()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/PDA10D_Calibrate/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            # Plot the output power measured using the PM100D
            laser_file = 'JDSU_DFB_T_20_Iso_PM100D.txt' # laser + isolator
            
            laser_5050_B = 'JDSU_DFB_T_20_Iso_PM100D_5050_Blue.txt' # laser + isolator + 50:50 splitter blue branch            
            laser_5050_B_90 = 'JDSU_DFB_T_20_Iso_PM100D_5050_Blue_9010_90.txt' # laser + isolator + 50:50 splitter blue branch + 90:10 splitter 90%
            laser_5050_B_10 = 'JDSU_DFB_T_20_Iso_PM100D_5050_Blue_9010_10.txt' # laser + isolator + 50:50 splitter blue branch + 90:10 splitter 10%

            laser_5050_Y = 'JDSU_DFB_T_20_Iso_PM100D_5050_Yellow.txt' # laser + isolator + 50:50 splitter yellow branch
            laser_5050_Y_90 = 'JDSU_DFB_T_20_Iso_PM100D_5050_Yellow_9010_90.txt' # laser + isolator + 50:50 splitter yellow branch + 90:10 splitter 90%
            laser_5050_Y_10 = 'JDSU_DFB_T_20_Iso_PM100D_5050_Yellow_9010_10.txt' # laser + isolator + 50:50 splitter yellow branch + 90:10 splitter 10%

            PLOT_STD_PM100D = False
            if PLOT_STD_PM100D:
                
                UNITS = False # make plot in mW
                col_choice = 2 if UNITS else 3

                # Make a multi-line plot
                hv_data = []; labels = []; marks = []; 
                
                L1 = numpy.loadtxt(laser_file, delimiter = '\t', unpack = True)
                hv_data.append([L1[0], L1[col_choice]]); labels.append('Laser + Iso Output'); marks.append(Plotting.labs_lins[0]); 
                
                LB = numpy.loadtxt(laser_5050_B, delimiter = '\t', unpack = True)
                hv_data.append([LB[0], LB[col_choice]]); labels.append('Blue 50%'); marks.append(Plotting.labs_lins[2]);

                LB90 = numpy.loadtxt(laser_5050_B_90, delimiter = '\t', unpack = True)
                hv_data.append([LB90[0], LB90[col_choice]]); labels.append('Blue 90%'); marks.append(Plotting.labs_lins[3]);

                LB10 = numpy.loadtxt(laser_5050_B_10, delimiter = '\t', unpack = True)
                hv_data.append([LB10[0], LB10[col_choice]]); labels.append('Blue 10%'); marks.append(Plotting.labs_lins[4]);
                
                LY = numpy.loadtxt(laser_5050_Y, delimiter = '\t', unpack = True)
                hv_data.append([LY[0], LY[col_choice]]); labels.append('Yellow 50%'); marks.append(Plotting.labs_lins[5]); 

                LY90 = numpy.loadtxt(laser_5050_Y_90, delimiter = '\t', unpack = True)
                hv_data.append([LY90[0], LY90[col_choice]]); labels.append('Yellow 90%'); marks.append(Plotting.labs_lins[6]);

                LY10 = numpy.loadtxt(laser_5050_Y_10, delimiter = '\t', unpack = True)
                hv_data.append([LY10[0], LY10[col_choice]]); labels.append('Yellow 10%'); marks.append(Plotting.labs_lins[1]);

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (mW)' if UNITS else 'Power (dBm)'
                args.fig_name = 'Power_PM100D_mW' if UNITS else 'Power_PM100D_dBm'

                Plotting.plot_multiple_curves(hv_data, args)

            # What is split ratio from 90:10 splitters? 
            # P_{90} = P_{10} + 9.34 (\pm 0.11) [dBm]
            PLOT_90_10_PM100D = True
            if PLOT_90_10_PM100D:
                
                UNITS = False # make plot in mW
                col_choice = 2 if UNITS else 3

                # Make a multi-line plot
                hv_data = []; labels = []; marks = []; 
                LB = numpy.loadtxt(laser_5050_B, delimiter = '\t', unpack = True)
                LB10 = numpy.loadtxt(laser_5050_B_10, delimiter = '\t', unpack = True)
                LB90 = numpy.loadtxt(laser_5050_B_90, delimiter = '\t', unpack = True)
                nn = len(LB10[col_choice])
                #hv_data.append([LB10[col_choice][1:nn], LB[col_choice][1:nn]]); labels.append('Blue 100'); marks.append(Plotting.labs_lins[2]);
                hv_data.append([LB10[col_choice][1:nn], LB90[col_choice][1:nn]]); labels.append('Blue 90:10'); marks.append(Plotting.labs[2]);

                # linear fit of P_90 vs P_10
                [mm, cc] = Common.linear_fit(numpy.asarray(LB10[col_choice][1:nn]), numpy.asarray(LB90[col_choice][1:nn]), [1,1], True)

                LY = numpy.loadtxt(laser_5050_Y, delimiter = '\t', unpack = True)
                LY10 = numpy.loadtxt(laser_5050_Y_10, delimiter = '\t', unpack = True)
                LY90 = numpy.loadtxt(laser_5050_Y_90, delimiter = '\t', unpack = True)
                #hv_data.append([LY10[col_choice][1:nn], LY[col_choice][1:nn]]); labels.append('Yellow 100'); marks.append(Plotting.labs_lins[5]);
                hv_data.append([LY10[col_choice][1:nn], LY90[col_choice][1:nn]]); labels.append('Yellow 90:10'); marks.append(Plotting.labs[5]);

                [mm, cc] = Common.linear_fit(numpy.asarray(LY10[col_choice][1:nn]), numpy.asarray(LY90[col_choice][1:nn]), [1,1], True)

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = '10% Power (mW)' if UNITS else '10% Power (dBm)'
                args.y_label = '90% Power (mW)' if UNITS else '90% Power (dBm)'
                args.fig_name = 'Power_9010_PM100D_mW' if UNITS else 'Power_9010_PM100D_dBm'

                Plotting.plot_multiple_curves(hv_data, args)

                # Combine the data sets to make a plot
                X = numpy.concatenate((LB10[col_choice][1:nn], LY10[col_choice][1:nn]), axis = None)
                Y = numpy.concatenate((LB90[col_choice][1:nn], LY90[col_choice][1:nn]), axis = None)
                print('Linear Fit')
                Common.linear_fit(numpy.asarray(X), numpy.asarray(Y), [1,1], True)

            # Can you fully recover P_{100} from P_{90} + P_{10}? 
            # Or what is the 90:10 splitter IL? 
            PLOT_90_10_IL = False
            if PLOT_90_10_IL:
                UNITS = True # make plot in mW
                col_choice = 2 if UNITS else 3

                # Make a multi-line plot
                hv_data = []; labels = []; marks = []; 
                LB = numpy.loadtxt(laser_5050_B, delimiter = '\t', unpack = True)
                LB10 = numpy.loadtxt(laser_5050_B_10, delimiter = '\t', unpack = True)
                LB90 = numpy.loadtxt(laser_5050_B_90, delimiter = '\t', unpack = True)
                nn = len(LB10[col_choice])
                
                hv_data.append([LB[0][1:nn], LB[col_choice][1:nn]]); labels.append('Blue 100%'); marks.append(Plotting.labs_lins[2]);
                hv_data.append([LB10[0][1:nn], LB90[col_choice][1:nn]]); labels.append('Blue 90%'); marks.append(Plotting.labs[2]);
                hv_data.append([LB10[0][1:nn], LB10[col_choice][1:nn]]); labels.append('Blue 10%'); marks.append(Plotting.labs_dashed[2]);

                LY = numpy.loadtxt(laser_5050_Y, delimiter = '\t', unpack = True)
                LY10 = numpy.loadtxt(laser_5050_Y_10, delimiter = '\t', unpack = True)
                LY90 = numpy.loadtxt(laser_5050_Y_90, delimiter = '\t', unpack = True)
                hv_data.append([LY[0][1:nn], LY[col_choice][1:nn]]); labels.append('Yellow 100%'); marks.append(Plotting.labs_lins[5]);
                hv_data.append([LY10[0][1:nn], LY90[col_choice][1:nn]]); labels.append('Yellow 90%'); marks.append(Plotting.labs[5]);                
                hv_data.append([LY10[0][1:nn], LY10[col_choice][1:nn]]); labels.append('Yellow 90%'); marks.append(Plotting.labs_dashed[5]);                

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Current (mA)'
                args.y_label = 'Power (mW)' if UNITS else 'Power (dBm)'
                args.fig_name = 'Power_1009010_mW' if UNITS else 'Power_1009010_dBm'

                Plotting.plot_multiple_curves(hv_data, args)

                # compute the IL
                ILB = []; ILY = []; 
                for i in range(1, nn, 1):
                    if UNITS:
                        ILB.append(LB90[col_choice][i] / LB[col_choice][i])
                        ILY.append(LY90[col_choice][i] / LY[col_choice][i])
                    else:
                        ILB.append( math.fabs(LB[col_choice][i]) - math.fabs(LB90[col_choice][i]) )
                        ILY.append( math.fabs(LY[col_choice][i]) - math.fabs(LY90[col_choice][i]) )

                hv_data = []; labels = []; marks = []; 
                hv_data.append([LY[0][1:nn], ILB]); labels.append('Blue IL'); marks.append(Plotting.labs[2])
                hv_data.append([LY[0][1:nn], ILY]); labels.append('Yellow IL'); marks.append(Plotting.labs[5])

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Current (mA)'
                args.y_label = 'IL (mW)' if UNITS else 'IL (dB)'
                args.fig_name = 'Power_9010_IL_mW' if UNITS else 'Power_9010_IL_dBm'

                Plotting.plot_multiple_curves(hv_data, args)
            
            # plot the output power measured using the PDA10CS
            laser_5050_BY_PDA10 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Blue_Yellow_G_0.txt' # laser + isolator + 50:50 splitter blue branch -> PDA1, yellow branch -> PDA2
            
            laser_5050_BY_PDA10_10_G_0 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Blue_Yellow_10_G_0.txt' # laser + isolator + 50:50 splitter blue branch -> 90:10 -> PDA1, yellow branch -> 90:10 -> PDA2, 10% arms, G = 0 dB
            laser_5050_BY_PDA10_10_G_10 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Blue_Yellow_10_G_10.txt' # laser + isolator + 50:50 splitter blue branch -> 90:10 -> PDA1, yellow branch -> 90:10 -> PDA2, 10% arms, G = 10 dB
            laser_5050_BY_PDA10_10_G_20 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Blue_Yellow_10_G_20.txt' # laser + isolator + 50:50 splitter blue branch -> 90:10 -> PDA1, yellow branch -> 90:10 -> PDA2, 10% arms, G = 20 dB

            laser_5050_YB_PDA10 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Yellow_Blue_G_0.txt' # laser + isolator + 50:50 splitter yellow branch -> PDA1, blue branch -> PDA2
            
            laser_5050_YB_PDA10_10_G_0 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Yellow_Blue_10_G_0.txt' # laser + isolator + 50:50 splitter yellow branch -> 90:10 -> PDA1, blue branch -> 90:10 -> PDA2, 10% arms, G = 0 dB
            laser_5050_YB_PDA10_10_G_10 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Yellow_Blue_10_G_10.txt' # laser + isolator + 50:50 splitter yellow branch -> 90:10 -> PDA1, blue branch -> 90:10 -> PDA2, 10% arms, G = 10 dB
            laser_5050_YB_PDA10_10_G_20 = 'JDSU_DFB_T_20_Iso_PDA10_5050_Yellow_Blue_10_G_20.txt' # laser + isolator + 50:50 splitter yellow branch -> 90:10 -> PDA1, blue branch -> 90:10 -> PDA2, 10% arms, G = 20 dB

            # plot the power as measured by the PDA10CS in units of V
            PLOT_STD_PDA10D = False
            if PLOT_STD_PDA10D:

                LBY = numpy.loadtxt(laser_5050_BY_PDA10, delimiter = '\t', unpack = True)
                LYB = numpy.loadtxt(laser_5050_YB_PDA10, delimiter = '\t', unpack = True)
                nn = len(LBY[0])

                hv_data = []; labels = []; marks = []; 
                hv_data.append([LBY[0], LBY[1] ]); labels.append('Blue 50% PD1'); marks.append(Plotting.labs_lins[2]); 
                hv_data.append([LYB[0], LYB[1] ]); labels.append('Yellow 50% PD1'); marks.append(Plotting.labs_lins[5]);
                
                hv_data.append([LYB[0], LYB[2] ]); labels.append('Blue 50% PD2'); marks.append(Plotting.labs_dashed[2]);
                hv_data.append([LBY[0], LBY[2] ]); labels.append('Yellow 50% PD2'); marks.append(Plotting.labs_dashed[5]);
                     
                
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Current (mA)'
                args.y_label = 'Power PDA10DCS (V)'
                args.fig_name = 'Power_PDA10DCS_V'

                Plotting.plot_multiple_curves(hv_data, args)

            # compare the power as measured in V to power as measured in units of mW
            PLOT_COMPAR_PDA10D = False
            if PLOT_COMPAR_PDA10D:
                UNITS = True # make plot in mW
                col_choice = 2 if UNITS else 3

                LB = numpy.loadtxt(laser_5050_B, delimiter = '\t', unpack = True)
                LY = numpy.loadtxt(laser_5050_Y, delimiter = '\t', unpack = True)
                LBY = numpy.loadtxt(laser_5050_BY_PDA10, delimiter = '\t', unpack = True)
                LYB = numpy.loadtxt(laser_5050_YB_PDA10, delimiter = '\t', unpack = True)
                nn = len(LBY[0])

                # linear fit of P_90 vs P_10
                print('B@PD1')
                Common.linear_fit(numpy.asarray(LBY[1][1:nn]), numpy.asarray(LB[col_choice][1:nn]), [1,1], True) # B@PD1 LBY[1][0:nn], LB[col_choice][0:nn]
                print('Y@PD1')
                Common.linear_fit(numpy.asarray(LYB[1][1:nn]), numpy.asarray(LY[col_choice][1:nn]), [1,1], True) # Y@PD1 LYB[1][0:nn], LY[col_choice][0:nn]
                print('B@PD2')
                Common.linear_fit(numpy.asarray(LYB[2][1:nn]), numpy.asarray(LB[col_choice][1:nn]), [1,1], True) # B@PD2 LYB[2][0:nn], LB[col_choice][0:nn]
                print('Y@PD2')
                Common.linear_fit(numpy.asarray(LBY[2][1:nn]), numpy.asarray(LY[col_choice][1:nn]), [1,1], True) # Y@PD2 LBY[2][0:nn], LY[col_choice][0:nn]

                hv_data = []; labels = []; marks = []; 
                hv_data.append([ LBY[1][1:nn], LB[col_choice][1:nn] ]); labels.append('Blue 50% PD1'); marks.append(Plotting.labs_lins[2]); 
                hv_data.append([ LYB[1][1:nn], LY[col_choice][1:nn] ]); labels.append('Yellow 50% PD1'); marks.append(Plotting.labs_lins[5]);
                # sample linear fit
                x_vals = [0, 3.5]; y_vals = [0, 3.5*0.83]; 
                hv_data.append([x_vals, y_vals]); labels.append('Avg PD1'); marks.append(Plotting.labs_lins[1]);
                
                hv_data.append([ LYB[2][1:nn], LB[col_choice][1:nn] ]); labels.append('Blue 50% PD2'); marks.append(Plotting.labs_dashed[2]);
                hv_data.append([ LBY[2][1:nn], LY[col_choice][1:nn] ]); labels.append('Yellow 50% PD2'); marks.append(Plotting.labs_dashed[5]);   
                # sample linear fit
                x_vals = [0, 3.5]; y_vals = [0, 3.5*0.63]; 
                hv_data.append([x_vals, y_vals]); labels.append('Avg PD2'); marks.append(Plotting.labs_dashed[1]);
                
                args = Plotting.plot_arg_multiple()

                args.loud = False
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Power PDA10DCS (V)'
                args.y_label = 'Power PM100D (mW)' if UNITS else 'Power PM100D (dBm)'
                args.fig_name = 'Power_PDA10DCS_PM100D_mW' if UNITS else 'Power_PDA10DCS_PM100D_dBm'

                Plotting.plot_multiple_curves(hv_data, args)

            # compare the power as measured in V to power as measured in units of mW on shared axes
            PLOT_COMPAR_TWO = False
            if PLOT_COMPAR_TWO:
                # make a two axis plot of the measured PDA10D data

                UNITS = True # make plot in mW
                col_choice = 2 if UNITS else 3

                LB = numpy.loadtxt(laser_5050_B, delimiter = '\t', unpack = True)
                LY = numpy.loadtxt(laser_5050_Y, delimiter = '\t', unpack = True)
                LBY = numpy.loadtxt(laser_5050_BY_PDA10, delimiter = '\t', unpack = True)
                LYB = numpy.loadtxt(laser_5050_YB_PDA10, delimiter = '\t', unpack = True)
                nn = len(LBY[0])

                args = Plotting.plot_arg_multiple()

                args.loud = False
                args.x_label = 'Current (mA)'
                args.y_label = 'Power PDA10DCS (V)'
                args.y_label_2 = 'Power PM100D (mw)'

                # B@PD1 LBY[1][0:nn], LB[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_B1_mW'
                args.plt_title = 'Power Branch B PD1'            
                Plotting.plot_two_axis(LBY[0][0:nn], LBY[1][0:nn], LB[col_choice][0:nn], args)
                print('B@PD1')
                Common.linear_fit(numpy.asarray(LBY[1][1:nn]), numpy.asarray(LB[col_choice][1:nn]), [1,1], True)
                
                # B@PD2 LYB[2][0:nn], LB[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_B2_mW'
                args.plt_title = 'Power Branch B PD2'            
                Plotting.plot_two_axis(LYB[0][0:nn], LYB[2][0:nn], LB[col_choice][0:nn], args)
                print('B@PD2')
                Common.linear_fit(numpy.asarray(LYB[2][1:nn]), numpy.asarray(LB[col_choice][1:nn]), [1,1], True)

                # Y@PD1 LYB[1][0:nn], LY[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_Y1_mW'
                args.plt_title = 'Power Branch Y PD1'            
                Plotting.plot_two_axis(LYB[0][0:nn], LYB[1][0:nn], LY[col_choice][0:nn], args)
                print('Y@PD1')
                Common.linear_fit(numpy.asarray(LYB[1][1:nn]), numpy.asarray(LY[col_choice][1:nn]), [1,1], True)
                
                # Y@PD2 LBY[2][0:nn], LY[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_Y2_mW'
                args.plt_title = 'Power Branch Y PD2'            
                Plotting.plot_two_axis(LBY[0][0:nn], LBY[2][0:nn], LY[col_choice][0:nn], args)
                print('Y@PD2')
                Common.linear_fit(numpy.asarray(LBY[2][1:nn]), numpy.asarray(LY[col_choice][1:nn]), [1,1], True)

            # compare the power measured through the 10% line in units of V and mW on shared axes
            PLOT_COMPAR_TEN = False
            if PLOT_COMPAR_TEN:
                UNITS = True # make plot in mW
                col_choice = 2 if UNITS else 3

                LB10 = numpy.loadtxt(laser_5050_B_10, delimiter = '\t', unpack = True) # B@10% on PM100D
                LY10 = numpy.loadtxt(laser_5050_Y_10, delimiter = '\t', unpack = True) # Y@10% on PM100D

                LBY10 = numpy.loadtxt(laser_5050_BY_PDA10_10_G_0, delimiter = '\t', unpack = True) # B@10%@PD1 and Y@10%@PD2
                LYB10 = numpy.loadtxt(laser_5050_YB_PDA10_10_G_0, delimiter = '\t', unpack = True) # B@10%@PD2 and Y@10%@PD1
                nn = len(LBY10[0])

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Current (mA)'
                args.y_label = 'Power PDA10DCS (V)'
                args.y_label_2 = 'Power PM100D (mw)'

                # B@PD1 LBY[1][0:nn], LB[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_B1_mW_10'
                args.plt_title = 'Power Branch B PD1'            
                Plotting.plot_two_axis(LBY10[0][0:nn], LBY10[1][0:nn], LB10[col_choice][0:nn], args)
                print('B@10%@PD1')
                Common.linear_fit(numpy.asarray(LBY10[1][1:nn]), numpy.asarray(LB10[col_choice][1:nn]), [1,1], True)

                # B@PD2 LYB[2][0:nn], LB[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_B2_mW_10'
                args.plt_title = 'Power Branch B PD2'            
                Plotting.plot_two_axis(LYB10[0][0:nn], LYB10[2][0:nn], LB10[col_choice][0:nn], args)
                print('B@10%@PD2')
                Common.linear_fit(numpy.asarray(LYB10[2][1:nn]), numpy.asarray(LB10[col_choice][1:nn]), [1,1], True)

                # Y@PD1 LYB[1][0:nn], LY[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_Y1_mW_10'
                args.plt_title = 'Power Branch Y PD1'            
                Plotting.plot_two_axis(LYB10[0][0:nn], LYB10[1][0:nn], LY10[col_choice][0:nn], args)
                print('Y@10%@PD1')
                Common.linear_fit(numpy.asarray(LYB10[1][1:nn]), numpy.asarray(LY10[col_choice][1:nn]), [1,1], True)
                
                # Y@PD2 LBY[2][0:nn], LY[col_choice][0:nn]
                args.fig_name = 'Power_PDA10DCS_PM100D_Y2_mW_10'
                args.plt_title = 'Power Branch Y PD2'            
                Plotting.plot_two_axis(LBY10[0][0:nn], LBY10[2][0:nn], LY10[col_choice][0:nn], args)
                print('Y@10%@PD2')
                Common.linear_fit(numpy.asarray(LBY10[2][1:nn]), numpy.asarray(LY10[col_choice][1:nn]), [1,1], True)

            # compare the power measured through the 10% line in units of V and mW on shared axes
            PLOT_COMPAR_TEN_AGAIN = False
            if PLOT_COMPAR_TEN_AGAIN:
                UNITS = True # make plot in mW
                col_choice = 2 if UNITS else 3

                LB = numpy.loadtxt(laser_5050_B_10, delimiter = '\t', unpack = True) # B@10% on PM100D
                LY = numpy.loadtxt(laser_5050_Y_10, delimiter = '\t', unpack = True) # Y@10% on PM100D

                LBY = numpy.loadtxt(laser_5050_BY_PDA10_10_G_0, delimiter = '\t', unpack = True) # B@10%@PD1 and Y@10%@PD2
                LYB = numpy.loadtxt(laser_5050_YB_PDA10_10_G_0, delimiter = '\t', unpack = True) # B@10%@PD2 and Y@10%@PD1
                nn = len(LBY[0])

                hv_data = []; labels = []; marks = []; 

                hv_data.append([ LBY[1][1:nn], LB[col_choice][1:nn] ]); labels.append('Blue 50% PD1'); marks.append(Plotting.labs_lins[2]); 
                hv_data.append([ LYB[1][1:nn], LY[col_choice][1:nn] ]); labels.append('Yellow 50% PD1'); marks.append(Plotting.labs_lins[5]);
                # sample linear fit
                #x_vals = [0, 0.35]; y_vals = [0, 0.35*0.8]; 
                #hv_data.append([x_vals, y_vals]); labels.append('Avg PD1'); marks.append(Plotting.labs_lins[1]);
                
                hv_data.append([ LYB[2][1:nn], LB[col_choice][1:nn] ]); labels.append('Blue 50% PD2'); marks.append(Plotting.labs_dashed[2]);
                hv_data.append([ LBY[2][1:nn], LY[col_choice][1:nn] ]); labels.append('Yellow 50% PD2'); marks.append(Plotting.labs_dashed[5]);   
                # sample linear fit
                #x_vals = [0, 0.35]; y_vals = [0, 0.35*0.62]; 
                #hv_data.append([x_vals, y_vals]); labels.append('Avg PD2'); marks.append(Plotting.labs_dashed[1]);
                
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Power PDA10DCS (V)'
                args.y_label = 'Power PM100D (mW)' if UNITS else 'Power PM100D (dBm)'
                args.fig_name = 'Power_PDA10DCS_PM100D_mW_10' if UNITS else 'Power_PDA10DCS_PM100D_dBm_10'

                Plotting.plot_multiple_curves(hv_data, args)

            # combine data sets to perform a true linear fit
            PLOT_LINEAR = False
            if PLOT_LINEAR:
                # Import data from an earlier measurement on a different laser
                current_loc = os.getcwd()

                ALT_HOME = 'c:/users/robertsheehan/Research/Laser_Physics/Data/DFB_Char/'
                os.chdir(ALT_HOME)

                # load in the pairs of data that you used to do calibration previously
                DFB1_PM1_1 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD1_1 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_Cal.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                DFB1_PM1_2 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_2.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD1_2 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_Cal_2.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1
                mm = len(DFB1_PD1_2[0])

                DFB1_PM1_3 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_Imax_30_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD1_3 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_Imax_30_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                DFB1_PM1_4 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_Imax_20_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD1_4 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_Imax_20_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                # PD2
                DFB1_PM2_1 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_Imax_20_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD2_1 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_2_Imax_20_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                DFB1_PM2_2 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_Imax_20_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD2_2 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_2_Imax_20_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                DFB1_PM2_3 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_Imax_30_2.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD2_3 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_2_Imax_30_G_0.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                DFB1_PM2_4 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_3.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD2_4 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_2_Cal_3.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                DFB1_PM2_5 = numpy.loadtxt('JDSU_CQF915_508_T_20_PM100D_S155C_Cal_4.txt', delimiter = '\t', unpack = True) # DFB power @PM100D
                DFB1_PD2_5 = numpy.loadtxt('JDSU_CQF915_508_T_20_PDA10CS_EC_2_Cal_4.txt', delimiter = '\t', unpack = True) # DFB power @PDA1_1

                ll = len(DFB1_PD2_5[0])

                os.chdir(current_loc)

                UNITS = True # make plot in mW
                col_choice = 2 if UNITS else 3

                LB = numpy.loadtxt(laser_5050_B, delimiter = '\t', unpack = True) # B@100% on PM100D
                LY = numpy.loadtxt(laser_5050_Y, delimiter = '\t', unpack = True) # Y@100% on PM100D

                LBY = numpy.loadtxt(laser_5050_BY_PDA10, delimiter = '\t', unpack = True) # B@100%@PD1 and Y@100%@PD2
                LYB = numpy.loadtxt(laser_5050_YB_PDA10, delimiter = '\t', unpack = True) # B@100%@PD2 and Y@100%@PD1

                LB10 = numpy.loadtxt(laser_5050_B_10, delimiter = '\t', unpack = True) # B@10% on PM100D
                LY10 = numpy.loadtxt(laser_5050_Y_10, delimiter = '\t', unpack = True) # Y@10% on PM100D

                LBY10 = numpy.loadtxt(laser_5050_BY_PDA10_10_G_0, delimiter = '\t', unpack = True) # B@10%@PD1 and Y@10%@PD2
                LYB10 = numpy.loadtxt(laser_5050_YB_PDA10_10_G_0, delimiter = '\t', unpack = True) # B@10%@PD2 and Y@10%@PD1
                nn = len(LBY10[0])

                # plot the data for PD1
                # B@PD1 LBY[1][0:nn], LB[col_choice][0:nn]
                # Y@PD1 LYB[1][0:nn], LY[col_choice][0:nn]
                X = numpy.concatenate((DFB1_PD1_1[1][1:mm], DFB1_PD1_2[1][1:mm], DFB1_PD1_3[1], DFB1_PD1_4[1], LBY[1][1:nn], LYB[1][1:nn], LBY10[1][1:nn], LYB10[1][1:nn]), axis = None)
                Y = numpy.concatenate((DFB1_PM1_1[col_choice][1:mm], DFB1_PM1_2[col_choice][1:mm], DFB1_PM1_3[col_choice], DFB1_PM1_4[col_choice], LB[col_choice][1:nn], LY[col_choice][1:nn], LB10[col_choice][1:nn], LY10[col_choice][1:nn]), axis = None)
                print('Linear Fit')
                Common.linear_fit(numpy.asarray(X), numpy.asarray(Y), [1,1], True)

                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'Power PDA10DCS (V)'
                args.y_label = 'Power PM100D (mW)'
                args.fig_name = 'Power_PDA10DCS_PM100D_mW_Combined_1'

                Plotting.plot_single_linear_fit_curve(X, Y, args)

                # B@PD2 LYB[2][0:nn], LB[col_choice][0:nn]
                # Y@PD2 LBY[2][0:nn], LY[col_choice][0:nn]
                X = numpy.concatenate((DFB1_PD2_1[1], DFB1_PD2_2[1], DFB1_PD2_3[1], DFB1_PD2_4[1][1:ll], DFB1_PD2_5[1], LYB[2][1:nn], LBY[2][1:nn], LYB10[2][1:nn], LBY10[2][1:nn]), axis = None)
                Y = numpy.concatenate((DFB1_PM2_1[col_choice], DFB1_PM2_2[col_choice], DFB1_PM2_3[col_choice], DFB1_PM2_4[col_choice][1:ll], DFB1_PM2_5[col_choice], LB[col_choice][1:nn], LY[col_choice][1:nn], LB10[col_choice][1:nn], LY10[col_choice][1:nn]), axis = None)
                print('Linear Fit')
                Common.linear_fit(numpy.asarray(X), numpy.asarray(Y), [1,1], True)

                args.fig_name = 'Power_PDA10DCS_PM100D_mW_Combined_2'

                Plotting.plot_single_linear_fit_curve(X, Y, args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate directory: ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Data_Frame_Aggregation():

    # Given multiple data frames that contain data from similar measurements of the same quantitie
    # How do you determine the averages, std. dev. of those data sets
    # How do you compute the average, std. dev. over multiple data frames? 
    # R. Sheehan 7 - 2 - 2024

    # Some notes
    # https://stackoverflow.com/questions/67583994/mean-and-standard-deviation-with-multiple-dataframes
    # https://stackoverflow.com/questions/29438585/element-wise-average-and-standard-deviation-across-multiple-dataframes
    
    # Generate some sample dataFrames, while adding an ID variable to track the original source
    nn = 4 # no. rows
    mm = 3 # no. columns
    df1 = pandas.DataFrame(numpy.random.randn(nn, mm), columns=['A', 'B', 'C']).assign(id='a')
    df2 = pandas.DataFrame(numpy.random.randn(nn, mm), columns=['A', 'B', 'C']).assign(id='b')
    df3 = pandas.DataFrame(numpy.random.randn(nn, mm), columns=['A', 'B', 'C']).assign(id='c')
    
    print('Sample DataFrame')
    print(df1)

    # Concatenate the existing df into a single df
    # Now you have three nn*mm df combined into a single 3*nn*mm dataframe
    # id column identifies the source of the dataframe so you haven't lost anything
    # can use id to access individual df
    df = pandas.concat([df1, df2, df3])

    print('\nConcatenated DataFrame')
    print(df)
    print('\nSelect Individual DataFrame')
    print(df[df['id']=='c'])

    # Use groupby to do any pandas method such as mean() or std() on an element by element basis
    dfavg = df.groupby('id').mean()
    print('\nAveraged DataFrame - Averaged in the sense that each column of the datasets is averaged')
    print("This isn't really what I want")
    print("Returned value is Average(A0, A1, A2) etc")
    print(dfavg)

    # Use groupby to do any pandas method such as mean() or std() on an element by element basis
    #dfavg = df.mean(axis=0)
    #df = pandas.DataFrame({'a': [1, 2], 'b': [3, 4]}, index=['tiger', 'zebra'])
    #print(df)
    #print('\nAveraged DataFrame - Average by Axis')
    #print('')    
    #print(df.mean(axis=0))
    #print(df.mean(axis=1))

    # It seems like it might come down to manipulating the df into the shape you want
    print('\nAveraged DataFrame - This is what I want')
    print(df['A'][0].mean(),',',df['B'][0].mean(),',',df['C'][0].mean())
    print(df['A'][1].mean(),',',df['B'][1].mean(),',',df['C'][1].mean())
    print(df['A'][2].mean(),',',df['B'][2].mean(),',',df['C'][2].mean())
    print(df['A'][3].mean(),',',df['B'][3].mean(),',',df['C'][3].mean())
    
    #print('\nStd. Dev. DataFrame - This is what I want')
    #print(df['A'][0].std(),',',df['B'][0].std(),',',df['C'][0].std())
    #print(df['A'][1].std(),',',df['B'][1].std(),',',df['C'][1].std())
    #print(df['A'][2].std(),',',df['B'][2].std(),',',df['C'][2].std())

    print('\nGeneral Average - of the type that I want')
    titles = list(df)
    # nn = no. rows of the data frame == no. distinct measurements = no. different data frames
    #for i in range(0, nn, 1):
    #    for j in range(0, len(titles)-1, 1):
    #        # this loop only goes to len(titles)-1 because you don't care about the id column
    #        print(df[ titles[j] ][i].mean(),',')
    #    print('\n')

    for j in range(0, len(titles)-1, 1):
        for i in range(0, nn, 1):
            print(i,',',titles[j],',',df[ titles[j] ][i].mean())

    #print('General Std. Dev.')
    #titles = list(df)
    #nn = 3
    #for i in range(0, nn, 1):
    #    for j in range(0, len(titles)-1, 1):
    #        print(df[titles[j]][i].std(),',')
    #    print('\n')

def Sorting_By_Column():

    # Want to be able to sort the data in an array by column
    # 

    a = numpy.array([ [1, 5, 9], [4, 0, 2], [2, 6, 7], [3, 3, 0] ])
    print("The array: ")
    print(a)

    print("The transposed array: ")
    print(a.T)

    print("\nSort: axis = None")
    print(numpy.sort(a, axis = None))

    print("\nSort: axis = 0")
    print(numpy.sort(a.T, axis = 0))

    print("\nSort: axis = 1")
    print(numpy.sort(a.T, axis = 1))

    print("\nSorting according to a column")
    print(a[a[:,0].argsort()])

def Plotting_With_Two_X_Axes():

    # Generating a plot with two x-axes


    pass

def Chilas_TLS_Characterisation():

    # Generate the plots from the Chilas TLS
    # R. Sheehan 30 - 4 - 2024

    FUNC_NAME = ".Chilas_TLS_Characterisation()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Data/Chilas_TLS/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            #os.chdir('Initial_Characterisation/')
            print(os.getcwd())

            PLOT_INIT_SPCTR = True
            if PLOT_INIT_SPCTR:
                the_dir = 'Initial_Characterisation/'
                the_files = []
                the_labels = []
                wl_list = numpy.arange(1500, 1590, 10)
                for i in range(0, len(wl_list), 1):
                    the_files.append('WL_%(v1)d.txt'%{"v1":int(wl_list[i]) })
                    the_labels.append(r'$\lambda_{s}$ = %(v1)d nm'%{"v1":int(wl_list[i]) })

                plt_title = 'Chilas TLS Output I = 250 mA'
                plt_name = 'Chilas_TLS_Output'

                #SpctrmPlt.multiple_optical_spectrum_plot(the_dir, the_files, the_labels, [1490, 1590, -80, +10], plt_title, plt_name, loudness = True)
                SpctrmPlt.multiple_optical_spectrum_plot(the_dir, the_files, the_labels, [1490, 1590, -80, +10], loudness = True)

            PLOT_INIT_VALS = False
            if PLOT_INIT_VALS:
                the_dir = 'Initial_Characterisation/'
                os.chdir(the_dir)
                data = numpy.loadtxt('OSA_Settings.txt', delimiter = '\t', skiprows = 6, usecols = [0, 1, 2, 3, 4], unpack = True)
                
                # Make plots of the measured quantities
                # plot power vs WL
                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'Wavelength (nm)'
                args.y_label = 'Optical Power (dBm)'
                args.fig_name = 'Optical_Power'
                args.plt_title = 'Chilas TLS Output I = 250 mA'

                Plotting.plot_single_curve(data[1], data[4], args)

                # plot SMSR and SNR versus WL
                args = Plotting.plot_arg_multiple()
                
                hv_data = [[data[1], data[3]], [data[1], data[2]]]
                labels = ['SNR', 'SMSR']
                marks = [Plotting.labs[0], Plotting.labs[1]]
                
                args.loud = True
                args.x_label = 'Wavelength (nm)'
                args.y_label = 'Ratio (dB)'
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.fig_name = 'Ratio'
                args.plt_title = 'Chilas TLS Output I = 250 mA'

                Plotting.plot_multiple_curves(hv_data,args)

            PLOT_HI_RES = False
            if PLOT_HI_RES:
                # Make plots of the hi-res spectrum
                # resolution = 0.05 nm, sensitivity = HIGH2
                # plot power vs WL

                the_dir = 'Initial_Characterisation/'
                os.chdir(the_dir)
                data = numpy.loadtxt('WL_1550_HiRes.txt', delimiter = '\t', unpack = True)

                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'Wavelength (nm)'
                args.y_label = 'Spectral Power (dBm / 0.05nm)'
                args.marker = Plotting.labs_lins[5]
                args.plt_range = [1548, 1552, -80, +10]
                args.fig_name = 'Optical_Power_HiRes'
                args.plt_title = 'Chilas TLS Output I = 250 mA'

                Plotting.plot_single_curve(data[0], data[1], args)

            PLOT_INIT_LINESHAPES = False
            if PLOT_INIT_LINESHAPES:
                the_dir = 'Initial_Characterisation/'
                os.chdir(the_dir)
                files = ['LLM_80.txt', 'LLM_160.txt', 'LLM_320.txt']
                fbeat = [80, 160, 320]
                hv_data = []
                labels = []
                marks = []
                count = 0
                for f in files:
                    data = numpy.loadtxt(f, delimiter = '\t', unpack = True)
                    data[0] = data[0] - fbeat[count]
                    hv_data.append(data); 
                    labels.append(r'$f_{b}$ = %(v1)d MHz'%{"v1":fbeat[count]}); 
                    marks.append(Plotting.labs_lins[count])
                    count = count + 1

                args = Plotting.plot_arg_multiple()
                
                args.loud = True
                args.x_label = 'Frequency Offset (MHz)'
                args.y_label = 'Spectral Power (dBm / 20kHz)'
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.fig_name = 'Lineshapes'
                args.plt_title = 'Chilas TLS Lineshape I = 250 mA'

                Plotting.plot_multiple_curves(hv_data, args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate directory: ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        
def CoBrite_TLS_Characterisation():

    # Generate the plots from the Chilas TLS
    # R. Sheehan 30 - 4 - 2024

    FUNC_NAME = ".CoBrite_TLS_Characterisation()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'C:/Users/robertsheehan/Research/Laser_Physics/Linewidth/Data/CPT_Tests/CoBriteTLS/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            #os.chdir('Initial_Characterisation/')
            print(os.getcwd())

            PLOT_INIT_SPCTR = True
            if PLOT_INIT_SPCTR:
                the_dir = 'Init_Char/'
                the_files = []
                the_labels = []
                plist = [6, 7, 8]
                for i in range(0, len(plist), 1):
                    the_files.append('OpticalOut_P_%(v1)ddBm.txt'%{"v1":plist[i] })
                    the_labels.append('P = %(v1)d dBm'%{"v1":plist[i] })

                plt_title = 'CoBrite TLS Output'
                plt_name = 'CoBrite_TLS_Output'

                SpctrmPlt.multiple_optical_spectrum_plot(the_dir, the_files, the_labels, [1545, 1555, -60, +10], plt_title, plt_name, loudness = True)
                #SpctrmPlt.multiple_optical_spectrum_plot(the_dir, the_files, the_labels, [1490, 1590, -80, +10], loudness = True)

            PLOT_INIT_LINESHAPES = False
            if PLOT_INIT_LINESHAPES:
                the_dir = 'Initial_Characterisation/'
                os.chdir(the_dir)
                files = ['LLM_80.txt', 'LLM_160.txt', 'LLM_320.txt']
                fbeat = [80, 160, 320]
                hv_data = []
                labels = []
                marks = []
                count = 0
                for f in files:
                    data = numpy.loadtxt(f, delimiter = '\t', unpack = True)
                    data[0] = data[0] - fbeat[count]
                    hv_data.append(data); 
                    labels.append(r'$f_{b}$ = %(v1)d MHz'%{"v1":fbeat[count]}); 
                    marks.append(Plotting.labs_lins[count])
                    count = count + 1

                args = Plotting.plot_arg_multiple()
                
                args.loud = True
                args.x_label = 'Frequency Offset (MHz)'
                args.y_label = 'Spectral Power (dBm / 20kHz)'
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.fig_name = 'Lineshapes'
                args.plt_title = 'Chilas TLS Lineshape I = 250 mA'

                Plotting.plot_multiple_curves(hv_data, args)

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate directory: ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        
def Paddy_Mac_Statistics():
    
    # Python implementation of the old Paddy Mac Statistics Lab
    # R. Sheehan 19 - 5 - 2025
    
    FUNC_NAME = ".Paddy_Mac_Statistics()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/robertsheehan/OneDrive - University College Cork/Documents/Teaching/PY4113/Re_ Radioactive Sources & Poisson Statistics/"
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())
            
            # The original data set of time intervals from P. MacCarthaig
            the_file = 'Rad_Decay_Raw_Time_Interval_Data.csv'            
            time_intervals = numpy.loadtxt(the_file, delimiter=',' ,unpack=True)
            n_data_pts = len(time_intervals) # total number of detected radioactive decay events (counts)
            
            # Newer data obtained by R. Sheehan May 2025
            # Data recorded is the time at which detection was measured
            # Data needs to be screened for time-intervals that are less than the detector dead-time and the DAQ sampling time
            GM_dead_time = 120e-6 # GM Tube dead time in units of s
            DAQ_sampling_time = 50e-6 # NI-USB-600 sampling time for SR = 20kHz
            the_file = 'Ra_5uC_Count_Data_1_1_plate_20_mins.txt'
            
            # data should be cleaned of any values that are greater than 1 and less than 0
            # decay probability is proportional to ( 1 / exp( Delta t ) )
            # Delta t > 1 => ( 1 / exp( Delta t ) ) is vanishingly small not physically correct
            # Delta t < 0 is also physically non-sensical
            # data should be cleaned of any blank / empty lines
            
            # Next step is to generate the cumulative sum of the data in the distribution
            # Do you actually need this an array? 
            # cum_sum_time = numpy.array([])
            # for i in range(0, n_data_pts):
            #     if i == 0:
            #         cum_sum_time = numpy.append(cum_sum_time, time_intervals[i])
            #     else:
            #         cum_sum_time = numpy.append(cum_sum_time,time_intervals[i] + cum_sum_time[i-1])
            
            # Find the cumulative sum of the data in the time interval distribution
            # This represents the total acquisition time
            t_acquire = 0 # total time over which radioactive decay events (counts) were detected
            for i in range(0, n_data_pts, 1):
                if i == 0:
                    t_acquire = time_intervals[i]
                else:
                    t_acquire = t_acquire + time_intervals[i]

            # Estimate the decay rate of the sample 
            decay_rate_approx = float(n_data_pts) / t_acquire # estimate of the decay rate
            
            # Estimate the error associated with the approximate decay rate
            decay_rate_error_estimate = decay_rate_approx / math.sqrt(float(n_data_pts)) # estimate the error associated with the approximate decay rate
            
            # Check for stationarity of the data
            n_bins = 200 # no. of subdivisions of the time_interval data, put optimal value here
            n_cnts_per_bin = n_data_pts / n_bins            
            theor_std_dev = math.sqrt( float( n_cnts_per_bin ) ) / decay_rate_approx # Poisson Statistics Standard Deviation 
            
            # Check for stationarity requires that you sub-divide the data into equal numbers of counts
            # note the time taken to acquire the counts in each of those bins
            # examining the distribution of those times
            #time_per_bin = numpy.zeros( n_bins )
            time_per_bin = numpy.array([])
            sum_val = 0.0
            # compute the sum of the time-intervals every n_cnts_per_bin
            for j in range(0, n_data_pts - int(n_cnts_per_bin), int(n_cnts_per_bin)):
                sum_val = 0.0
                for i in range(0, int(n_cnts_per_bin), 1):
                    if i == 0:
                        sum_val = time_intervals[j+i]
                    else:
                        sum_val = sum_val + time_intervals[j+(i-1)]
                time_per_bin = numpy.append(time_per_bin, sum_val)
                
            exp_average = numpy.mean(time_per_bin)
            exp_std_dev = numpy.std(time_per_bin, ddof = 1) # one estimate for the experimental std. dev.
            
            # what is the variance of the variance? 
            # no idea what's going on with this, theor_var_var_3 gives the closest value to exp_var_var
            # theor_var_var_2 is way off as expected
            # theor_var_var_4 is meant to give the closest value but is off by factor of 10
            # theor_var_var_5 and theor_var_var_5 are both off by factor of 100
            exp_var_var = math.sqrt( math.fabs( (exp_std_dev**2) - (theor_std_dev**2) ) )
            theor_var_var_2 = math.sqrt( (2.0*float(n_data_pts)**2 + 6.0*float(n_data_pts) )  / decay_rate_approx**4 ) # Erlang Distribution Standard Deviation?
            theor_var_var_3 = math.sqrt( ( 2.0*float(n_cnts_per_bin)**2 + 6.0*float(n_cnts_per_bin) )  / ( decay_rate_approx**4) ) # Erlang Distribution Standard Deviation?
            theor_var_var_4 = math.sqrt( ( 2.0*float(n_cnts_per_bin)**2 + 6.0*float(n_cnts_per_bin) )  / ( (n_bins - 1 ) * decay_rate_approx**4) ) # Erlang Distribution Standard Deviation?
            theor_var_var_5 = math.sqrt( ( 2.0*float(n_data_pts)**2 + 6.0*float(n_data_pts) )  / ( (n_bins - 1 ) * decay_rate_approx**4) ) # Erlang Distribution Standard Deviation?
            theor_var_var_6 = math.sqrt( ( 2.0*float(n_data_pts)**2 + 6.0*float(n_data_pts) )  / ( (n_cnts_per_bin - 1 ) * decay_rate_approx**4) ) # Erlang Distribution Standard Deviation?
            
            # The point here is to examine the effect of the no. of bins on the distribution of the data? 
            # You can show there is a difference between the theoretical and the experimental time-per-bin std. dev. 
            # based on the value of the no. of bins
            # Make it a task to optimise the no. of bins? 
            # What does the exp. std. dev. look like for different bin no?    
            bins_arr = numpy.arange(50, 420, 25)
            stdev_diff = numpy.zeros( len(bins_arr) )
            for k in range(0, len(bins_arr), 1):
                counts_per_bin = n_data_pts / bins_arr[k]
                time_in_bin = numpy.array([])
                sum_val = 0.0
                # compute the sum of the time-intervals every n_cnts_per_bin
                for j in range(0, n_data_pts - int(counts_per_bin), int(counts_per_bin)):
                    sum_val = 0.0
                    for i in range(0, int(counts_per_bin), 1):
                        if i == 0:
                            sum_val = time_intervals[j+i]
                        else:
                            sum_val = sum_val + time_intervals[j+(i-1)]
                    time_in_bin = numpy.append(time_in_bin, sum_val)
                # store the experimental std. dev. for each value of no. bins
                stdev_diff[k] = math.fabs( theor_std_dev - numpy.std(time_in_bin,ddof = 1) )
                del time_in_bin
            
            print()
            print('Data Set Report')
            print(the_file,'contains',n_data_pts,'data points')
            print('The file contains the time intervals between',n_data_pts,'successive radioactive decays detected by the Geiger counter.')
            print('Longest time between decays: %(v1)0.6f secs'%{"v1":numpy.max(time_intervals)})
            print('Shortest time between decays: %(v1)0.6f secs'%{"v1":numpy.min(time_intervals)})
            print('Shortest time between decays: %(v1)0.3f usecs'%{"v1":1e+6*numpy.min(time_intervals)})
            print('Average time between decays: %(v1)0.6f secs'%{"v1":numpy.mean(time_intervals)})
            print('Std. Dev of time between decays: %(v1)0.6f secs'%{"v1":numpy.std(time_intervals, ddof = 1)})
            print('Median time between decays: %(v1)0.6f secs'%{"v1":numpy.median(time_intervals)})
            print()
                        
            # the mode of the distribution is the most common value
            # determine the mode of the distribution, this may not be unique
            #print(scipy.stats.mode(time_intervals)) 
            
            print('Approximation of the Decay rate')
            print('Duration of Experiment: %(v1)0.6f secs'%{"v1":t_acquire})
            print('Duration of Experiment: %(v1)0.6f mins'%{"v1":t_acquire/60.0})
            print('Approximate Decay Rate of the Sample: %(v1)0.2f +/- %(v2)0.2f per sec'%{"v1":decay_rate_approx,"v2":decay_rate_error_estimate})
            print()
            
            print('Check for stationarity')
            print('No. bins: %(v1)d'%{"v1":n_bins})
            print('No. counts per bin: %(v1)d'%{"v1":n_cnts_per_bin})
            print('Average time per bin: %(v1)0.6f secs'%{"v1":exp_average})
            #print('Average time per bin: %(v1)0.2f +/- %(v2)0.2f secs'%{"v1":exp_average,"v2":exp_std_dev} )
            print('Experimental Std. Dev.: %(v1)0.6f secs'%{"v1":exp_std_dev})
            print('Theoretical Std. Dev.: %(v1)0.6f secs'%{"v1":theor_std_dev})
            print('Delta Std. Dev.: %(v1)0.6f secs'%{"v1":math.fabs(theor_std_dev - exp_std_dev)})
            print()
            
            print('Examine the Variance of the Variance')
            print('Experimental Std. Dev. of Variance: %(v1)0.6f secs'%{"v1":exp_var_var})
            print('Theoretical Std. Dev. of Variance: %(v1)0.6f secs'%{"v1":theor_var_var_3})
            print('Theoretical Std. Dev. of Variance: %(v1)0.6f secs'%{"v1":theor_var_var_2})    
            print('Theoretical Std. Dev. of Variance: %(v1)0.6f secs'%{"v1":theor_var_var_4})    
            print('Theoretical Std. Dev. of Variance: %(v1)0.6f secs'%{"v1":theor_var_var_5})    
            print('Theoretical Std. Dev. of Variance: %(v1)0.6f secs'%{"v1":theor_var_var_6})    
            print()

            # Make a plot of the time-interval data
            PLOT_TIME_INTS = True
            if PLOT_TIME_INTS:                
                x_vals = numpy.arange(0, n_data_pts, 1)
                args = Plotting.plot_arg_single()
                args.loud = True
                args.x_label = 'Decay No.'
                args.y_label = 'Time Between Decays (secs)'
                args.fig_name = 'Times_Interval_Values_%(v1)s'%{"v1":the_file.replace('.csv','')}

                Plotting.plot_single_curve(x_vals, time_intervals, args)

            # Make a histogram of the time-interval data
            PLOT_HIST = False
            if PLOT_HIST:
                args = Plotting.plot_arg_single()
                args.loud = True
                args.bins = n_bins
                args.x_label = 'Time Intervals (secs)'
                args.y_label = 'No. Decays per Time Interval'
                args.plt_title = 'Approximate Decay Rate: %(v1)0.2f +/- %(v2)0.2f per sec'%{"v1":decay_rate_approx,"v2":decay_rate_error_estimate}
                args.fig_name = 'Histogram_%(v1)s'%{"v1":the_file.replace('.csv','')}
                Plotting.plot_histogram(time_intervals, args)

            # Make a plot of the time-per-bin data
            PLOT_TIMES = False
            if PLOT_TIMES:                
                x_vals = numpy.arange(0, n_bins, 1)
                args = Plotting.plot_arg_single()
                args.loud = True
                args.x_label = 'Bin No.'
                args.y_label = 'Time per Bin (secs)'
                args.plt_title = 'Average time per bin: %(v1)0.2f +/- %(v2)0.2f secs'%{"v1":exp_average,"v2":exp_std_dev}
                args.fig_name = 'Times_Per_Bin_%(v1)s'%{"v1":the_file.replace('.csv','')}
                args.plt_range = [0, n_bins, 0, 7]

                Plotting.plot_single_curve(x_vals, time_per_bin, args)
            
            # Make a plot of the std. difference as function of no. bins
            PLOT_STDEV = False
            if PLOT_STDEV:
                args = Plotting.plot_arg_single()
                args.loud = True
                args.x_label = 'Number of Bins'
                args.y_label = r'$\|\sigma_{theor} - \sigma_{exp}\|$ (secs)'
                args.plt_title = ''
                args.fig_name = 'Delta_Stdev_%(v1)s'%{"v1":the_file.replace('.csv','')}
                
                Plotting.plot_single_curve(bins_arr, stdev_diff, args)

            del time_intervals; del time_per_bin; del bins_arr; del stdev_diff;
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nCannot find:"+DATA_HOME
            raise(Exception)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Micram_DAC4_Characterisation():
    
    # Make plots of the Micram DAC4 AWG characterisation data
    # R. Sheehan 26 - 6 - 2025

    FUNC_NAME = ".Micram_DAC4_Characterisation()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Programming/MATLAB/Micram_AWG/'; 
    
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())
            
            sqr_file = 'Square_Pulse_Width_Char_25_6_2025_Nw_5_Nd_10.txt'
            twp_file = 'Twin_Pulse_Width_Char_25_6_2025_Nw_%(v1)d_Nd_%(v2)d.txt'

            # Plot Square-Wave Meas
            PLOT_SQR = False
            if PLOT_SQR:
                sqr_data = numpy.loadtxt(sqr_file, comments='#', delimiter = ',', unpack = True)
                
                # Make a plot of the measured sq-wave output frq versus clock frequency
                args = Plotting.plot_arg_single(); 
        
                args.loud = True
                args.x_label = 'Clock Frequency (GHz)'
                args.y_label = 'Square Wave Frequency (GHz)'
                args.plt_title = 'Nw = 5, Nd = 10'
                args.fig_name = sqr_file.replace(".txt","") + '_Output_Meas_Frq'
                args.plt_range = [1, 37, 0, 5]
                
                Plotting.plot_single_linear_fit_curve(sqr_data[0], sqr_data[5], args)

                # Make a linear fit of the measured sq-wave output frq versus clock frequency
                Common.linear_fit(sqr_data[0], sqr_data[5], [1,1], True)
                
                # Make a plot of the ratio of pulse separation to pulse width
                # In this case the pulse separation should be twice the pulse width
                NW = 5; ND = 10; 
                Micram_Plot_Ratio(sqr_file, NW, ND)
                
                # Make a plot of the measured pulse width and measured separation versus clock frequency
                Micram_Plot_Two_Times(sqr_file, NW, ND)
                
                # Make a plot of of the inverse measured pulse width versus clock Frequency
                Micram_Plot_Inverse_Pulse_Width(sqr_file, NW, ND)
                
            # Plot Twin-Pulse versus Square-Wave Data
            PLOT_TP_SQR = True
            if PLOT_TP_SQR:
                nwlist = [5, 5, 6, 6]
                ndlist = [10, 20, 12, 24]
                
                filelist = []
                labels = []
                filelist.append(sqr_file); labels.append('Sqr Nw = 5, Nd = 10'); 
                for i in range(0, len(nwlist), 1):
                    filename = twp_file%{"v1":nwlist[i], "v2":ndlist[i]}
                    if glob.glob(filename):
                        filelist.append(filename)
                        labels.append( 'Twn Nw = %(v1)d, Nd = %(v2)d'%{"v1":nwlist[i], "v2":ndlist[i]} ); 
                        #Micram_Plot_Two_Times(filename, nwlist[i], ndlist[i])
                        #Micram_Plot_Ratio(filename, nwlist[i], ndlist[i])
                        #Micram_Plot_Inverse_Pulse_Width(filename, nwlist[i], ndlist[i])
                    
                # Plot the pulse widths relative to the square wave
                #Micram_Plot_Multiple_Pulses(filelist, labels, col_choice = 1)     
                Micram_Plot_Multiple_Inverse_Pulses(filelist, labels, col_choice = 1)
                        
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate ' + DATA_HOME
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        
def Micram_Plot_Two_Times(filename, Nw, Nd):

    # Make a plot of the micram pulse width and pulse delay data on the same graph
    # R. Sheehan 27 - 6 - 2025

    FUNC_NAME = ".Micram_Plot_Two_Times()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME
    
    try:
        if glob.glob(filename):
            
            data = numpy.loadtxt(filename, comments='#', delimiter = ',', unpack = True)

            # Make a plot of the measured pulse width and measured separation versus clock frequency
            hv_data = []; labels = []; marks = []; 
            hv_data.append([data[0], data[1], data[2]/10.0]); labels.append('Pulse Width'); marks.append(Plotting.labs_pts[0]); 
            hv_data.append([data[0], data[3], data[4]/10.0]); labels.append('Pulse Separation'); marks.append(Plotting.labs_pts[1]);
        
            args = Plotting.plot_arg_multiple()
                
            args.loud = True
            args.x_label = 'Clock Frequency (GHz)'
            args.y_label = 'Pulse Timing (ps)'
            args.plt_title = 'Nw = %(v1)d, Nd = %(v2)d'%{"v1":Nw, "v2":Nd}
            args.fig_name = filename.replace(".txt","") + '_Meas_Pulse_Timings'
            args.mrk_list = marks
            args.crv_lab_list = labels
            args.plt_range = [1, 25, 0, 2000]
                
            Plotting.plot_multiple_curves_with_errors(hv_data, args)
        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate file: ' + filename
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        
def Micram_Plot_Multiple_Pulses(filelist, labels, col_choice):

    # Make a plot of the micram pulse width data for multiple files
    # R. Sheehan 27 - 6 - 2025

    FUNC_NAME = ".Micram_Plot_Multiple_Pulses()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME
    
    try:
        # read and store the data
        hv_data = []
        marks = []
        for i in range(0, len(filelist), 1):
            data = numpy.loadtxt(filelist[i], comments='#', delimiter = ',', unpack = True)
            hv_data.append([data[0], data[col_choice], data[col_choice+1]/10.0]); 
            marks.append(Plotting.labs_pts[i])
        
        # Make a plot of the pulse width data
        args = Plotting.plot_arg_multiple()
        
        args.loud = True
        args.x_label = 'Clock Frequency (GHz)'
        args.y_label = 'Pulse Width (ps)' if col_choice == 1 else 'Pulse Separation (ps)'
        args.fig_name = 'Pulse_Widths_Zm' if col_choice == 1 else 'Pulse_Separations'
        args.mrk_list = marks
        args.crv_lab_list = labels
        args.plt_range = [7, 25, 100, 400] if col_choice == 1 else [1, 25, 0, 2000]
                
        Plotting.plot_multiple_curves_with_errors(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        
def Micram_Plot_Multiple_Inverse_Pulses(filelist, labels, col_choice):

    # Make a plot of the micram inverse pulse width data for multiple files
    # R. Sheehan 30 - 6 - 2025

    FUNC_NAME = ".Micram_Plot_Multiple_Inverse_Pulses()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME
    
    try:
        # read and store the data
        hv_data = []
        marks = []
        count = 0
        for i in range(0, len(filelist), 1):
            data = numpy.loadtxt(filelist[i], comments='#', delimiter = ',', unpack = True)
            z, dz = Compute_Inverse_Data(data[col_choice], data[col_choice+1]) # compute the inverse data and its error
            hv_data.append([data[0], z, dz]); 
            marks.append(Plotting.labs_pts[count])
            count = count + 1
        
        # Make a plot of the pulse width data
        args = Plotting.plot_arg_multiple()
        
        args.loud = True
        args.x_label = 'Clock Frequency (GHz)'
        args.y_label = 'Pulse Width (GHz)' if col_choice == 1 else 'Pulse Separation (GHz)'
        args.fig_name = 'Inverse_Pulse_Widths' if col_choice == 1 else 'Inverse_Pulse_Separations'
        args.mrk_list = marks
        args.crv_lab_list = labels
        args.plt_range = [0, 37, 0, 15] if col_choice == 1 else [1, 25, 0, 2000]
                
        Plotting.plot_multiple_curves_with_errors(hv_data, args)
        #Plotting.plot_multiple_linear_fit_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Micram_Plot_Ratio(filename, Nw, Nd):
    
    # Make a plot of the pulse delay / width ratio
    # R. Sheehan 27 - 6 - 2025

    FUNC_NAME = ".Micram_Plot_Ratio()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(filename):
            data = numpy.loadtxt(filename, comments='#', delimiter = ',', unpack = True)
            
            # Make a plot of the ratio of pulse separation to pulse width
            # In this case the pulse separation should be twice the pulse width
            
            args = Plotting.plot_arg_single()
            
            args.loud = True
            args.x_label = 'Clock Frequency (GHz)'
            args.y_label = 'Separation / Width'
            args.plt_title = 'Nw = %(v1)d, Nd = %(v2)d'%{"v1":Nw, "v2":Nd}
            args.fig_name = filename.replace(".txt","") + '_Sep_Width_Ratio'
            args.plt_range = [1, 25, 1, 5]

            # Given the quantity z = x / y the error associated with z is given by 
            # (delta z / z)^{2} = (delta x / x)^{2} + (delta y / y)^{2}
            z = numpy.zeros( len(data[1]) )
            dz = numpy.zeros( len(data[1]) )
            for i in range(0, len(data[1]), 1):
                z[i] = ( data[3][i] / data[1][i] )
                dz[i] = z[i] * math.sqrt( ( (data[2][i]/10.0) / data[1][i] )**2 + 
                                            ( (data[4][i]/10.0) / data[3][i] )**2 )
                
            Plotting.plot_single_linear_fit_curve_with_errors(data[0], z, dz, args)
                
            # Make a linear fit of the measured sq-wave (separation / width ) versus clock frequency
            Common.linear_fit(data[0], z, [1,1], True)

            del data; del z; del dz; 

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate file: ' + filename
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Micram_Plot_Inverse_Pulse_Width(filename, Nw, Nd):
    
    # Make a plot of the inverse of the pulse width
    # R. Sheehan 30 - 6 - 2025

    FUNC_NAME = ".Micram_Plot_Inverse_Pulse_Width()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(filename):
            data = numpy.loadtxt(filename, comments='#', delimiter = ',', unpack = True)
            
            # Make a plot of the ratio of pulse separation to pulse width
            # In this case the pulse separation should be twice the pulse width
            
            args = Plotting.plot_arg_single()
            
            args.loud = True
            args.x_label = 'Clock Frequency (GHz)'
            args.y_label = 'Pulse Width (GHz)'
            args.plt_title = 'Nw = %(v1)d, Nd = %(v2)d'%{"v1":Nw, "v2":Nd}
            args.fig_name = filename.replace(".txt","") + '_Inverse_Pulse_Width'
            #args.plt_range = [1, 25, 1, 5]

            # Given the quantity z = 1 / y the error associated with z is given by 
            # (delta z / z)^{2} = (delta y / y)^{2} => delta z = delta y / y^{2}
            # z = numpy.zeros( len(data[1]) )
            # dz = numpy.zeros( len(data[1]) )
            # for i in range(0, len(data[1]), 1):
            #     z[i] = ( 1000.0 / data[1][i] ) # convert pulse width in (ps) to pulse width in (GHz)
            #     dz[i] = (z[i]/ data[1][i]) * (data[4][i]/10.0) # convert the timing error from (ps) to (GHz)
            
            z, dz = Compute_Inverse_Data(data[1], data[2])
                
            Plotting.plot_single_linear_fit_curve_with_errors(data[0], z, dz, args)
            #Plotting.plot_single_curve(data[0], z, args)
                
            # Make a linear fit of the measured sq-wave (separation / width ) versus clock frequency
            Common.linear_fit(data[0], z, [1,1], True)

            del data; del z; del dz; 

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate file: ' + filename
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Compute_Inverse_Data(y, deltay):
    
    # Given the set of (y, delta-y) data, compute its inverse
    # R. Sheehan 30 - 6 - 2025

    FUNC_NAME = ".Compute_Inverse_Data()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if len(y) > 0 else False
        c2 = True if len(deltay) > 0 else False
        c3 = True if len(y) == len(deltay) else False
        c10 = c1 and c2 and c3
        
        if c10:
            # Given the quantity z = 1 / y the error associated with z is given by 
            # (delta z / z)^{2} = (delta y / y)^{2} => delta z = delta y / y^{2}
            z = numpy.zeros( len(y) )
            dz = numpy.zeros( len(y) )
            for i in range(0, len(y), 1):
                z[i] = ( 1000.0 / y[i] ) # convert pulse width in (ps) to pulse width in (GHz)
                dz[i] = (z[i]/ y[i]) * (deltay[i]/10.0) # convert the timing error from (ps) to (GHz)
            return [z, dz]
        else:
            if c1 or c2 or c3:
                ERR_STATEMENT = ERR_STATEMENT + '\nInput arrays not sized correctly\n'
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        
def PI_Poster_2025():
    
    # Make the plots for the PI Poster 2025
    # R. Sheehan 21 - 8 - 2025
    
    FUNC_NAME = ".PI_Poster_2025()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Publications/Photonics_Ireland_2025/'; 
    
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())
            
        # Take a look at the long time measurement data
        PLOT_LONG = False
        
        if PLOT_LONG:
            LDC_Long = numpy.loadtxt("Power_mW_Data_LDC210C_75mA_T_25C_1hr_30s.txt")
            SMD_Long = numpy.loadtxt("Vload_V_Power_mW_Data_IBM4_75mA_T_25C_60min_30s.txt", delimiter = '\t', unpack = True)
            K2602_Long = numpy.loadtxt("Vload_V_Power_mW_Data_K2602_75mA_T_25C_60min_30s.txt", delimiter = '\t', unpack = True)
            
            # Optical Power
            LDC_avg_p = numpy.mean(LDC_Long); LDC_err_p = numpy.std(LDC_Long,ddof = 1); LDC_var_p = numpy.var(LDC_Long,ddof = 1); 
            SMD_avg_p = numpy.mean(SMD_Long[1]); SMD_err_p = numpy.std(SMD_Long[1],ddof = 1); SMD_var_p = numpy.var(SMD_Long[1],ddof = 1); 
            K2602_avg_p = numpy.mean(K2602_Long[1]); K2602_err_p = numpy.std(K2602_Long[1],ddof = 1); K2602_var_p = numpy.var(K2602_Long[1],ddof = 1); 

            print("\nMeasured Power at I = 75 ( mA ) and T = 25 C")
            print("LDC Power = %(v1)0.3f +/- %(v2)0.3f ( mW )"%{"v1":LDC_avg_p, "v2":LDC_err_p})
            print("K2602 Power = %(v1)0.3f +/- %(v2)0.3f ( mW )"%{"v1":K2602_avg_p, "v2":K2602_err_p})
            print("SMD Power = %(v1)0.3f +/- %(v2)0.3f ( mW )"%{"v1":SMD_avg_p, "v2":SMD_err_p})
            print("Power Difference = %(v1)0.2f"%{"v1":K2602_avg_p - SMD_avg_p})
                        
            print("\nMeasured Variances")
            print("LDC Power Var = %(v1)0.3f ( uW )"%{"v1":1000*LDC_var_p})
            print("K2602 Power Var = %(v1)0.3f ( uW )"%{"v1":1000*K2602_var_p})
            print("SMD Power Var = %(v1)0.3f ( uW )"%{"v1":1000*SMD_var_p})
            
            # Diode Voltage
            SMD_avg_v = numpy.mean(SMD_Long[0]); SMD_err_v = numpy.std(SMD_Long[0],ddof = 1); 
            K2602_avg_v = numpy.mean(K2602_Long[0]); K2602_err_v = numpy.std(K2602_Long[0],ddof = 1);
            
            print("\nMeasured Voltage at I = 75 ( mA ) and T = 25 C")
            print("K2602 Vload = %(v1)0.4f +/- %(v2)0.4f ( V )"%{"v1":K2602_avg_v, "v2":K2602_err_v})
            print("SMD Vload = %(v1)0.4f +/- %(v2)0.4f ( v )"%{"v1":SMD_avg_v, "v2":SMD_err_v})
            print("Voltage Difference = %(v1)0.3f"%{"v1":K2602_avg_v - SMD_avg_v})
            
            # Scale the data for zero mean and unity sigma
            SMD_scl_data = (SMD_Long[1] - SMD_avg_p) / SMD_err_p
            LDC_scl_data = (LDC_Long - LDC_avg_p) / LDC_err_p
            K2602_scl_data = (K2602_Long[1] - K2602_avg_p) / K2602_err_p

            RUN_F_TEST = False
            if RUN_F_TEST:
                # Use the F-test to determine if there is a significant difference between the distribution standard deviations
                # Apparently, F-test is only good is data is normal
                # Use Levene test instead
                # https://stackoverflow.com/questions/21494141/how-do-i-do-a-f-test-in-python
            
                """
                https://en.wikipedia.org/wiki/Levene%27s_test
                In statistics, Levene's test is an inferential statistic used to assess the equality of variances for a variable calculated for two or more groups. This test is used because some common
                statistical procedures assume that variances of the populations from which different samples are drawn are equal. Levene's test assesses this assumption. It tests the null hypothesis
                that the population variances are equal (called homogeneity of variance or homoscedasticity). If the resulting p-value of Levene's test is less than some significance level (typically
                0.05), the obtained differences in sample variances are unlikely to have occurred based on random sampling from a population with equal variances. Thus, the null hypothesis of equal
                variances is rejected and it is concluded that there is a difference between the variances in the population. 
                """
            
                #F_stat = (SMD_err_p**2) / (K2602_err_p**2) # 
                #df1 = len(SMD_Long[1]-1)
                #df2 = len(K2602_Long[1]-1)         
                #alpha = 0.05 # significance level
                # p_value = 1.0 - scipy.stats.f.sf(F_stat, df1, df2)
                #stat, p_value = scipy.stats.bartlett(SMD_Long[1], K2602_Long[1])
            
                alpha = 0.05 # significance level
                stat, p_value = scipy.stats.levene(SMD_Long[1], K2602_Long[1])
                print("\np_value = %(v1)0.9f"%{"v1":p_value})
                print("K2602 Power Var = %(v1)0.9f ( mW )"%{"v1":K2602_var_p})
                print("SMD Power Var = %(v1)0.9f ( mW )"%{"v1":SMD_var_p})
                if p_value < alpha:
                    print("The obtained differences in sample variances are unlikely to have occurred based on random sampling from a population with equal variances")
                    print("The null hypothesis of equal variances is rejected and it is concluded that there is a difference between the variances in the population")
                else:
                    print("The null hypothesis of equal variances is accepted.\n It is concluded that there is no difference between the variances in the population.")
            
                stat, p_value = scipy.stats.levene(SMD_Long[1], LDC_Long)
                print("\np_value = %(v1)0.9f"%{"v1":p_value})
                print("LDC Power Var = %(v1)0.9f ( mW )"%{"v1":LDC_var_p})
                print("SMD Power Var = %(v1)0.9f ( mW )"%{"v1":SMD_var_p})
                if p_value < alpha:
                    print("The obtained differences in sample variances are unlikely to have occurred based on random sampling from a population with equal variances")
                    print("The null hypothesis of equal variances is rejected and it is concluded that there is a difference between the variances in the population")
                else:
                    print("The null hypothesis of equal variances is accepted.\n It is concluded that there is no difference between the variances in the population.")
            

            # Make a histogram of the data
            # scale the data horizontally so that the distributions sit on top of one another
            # emphasise the similarities between the distributions

            # Use Sturges' Rule to compute the no. of bins required
            n_bins = int( 1.0 + 3.322*math.log( len(LDC_Long) ) )

            PLOT_SCALED_HIST = True
            if PLOT_SCALED_HIST:
                plt.hist(SMD_scl_data, bins = n_bins, label = r'SMD $\sigma$ = 2 $\mu$W', alpha=0.9, color = 'red', edgecolor = 'black', linestyle = '-')
                #plt.hist(LDC_scl_data, bins = n_bins, label = r'LDC210C $\sigma$ = 1 $\mu$W', alpha=0.65, color = 'red' , edgecolor = 'black', linestyle = '--')
                plt.hist(K2602_scl_data, bins = n_bins, label = r'K2602 $\sigma$ = 3 $\mu$W', alpha=0.6, color = 'green', edgecolor = 'black', linestyle = ':' )
                plt.xlim(xmin=-2.5, xmax = 2.5)
                plt.xlabel(r'Scaled Measurements $( P_{i} - \mu ) / \sigma$', fontsize = 14)
                plt.ylabel('Counts', fontsize = 14)
                plt.legend(loc = 'best')
                plt.savefig('Scaled_Power_Hist')
                plt.show()            
                plt.clf()
                plt.cla()
                plt.close()
            else:
                plt.hist(SMD_Long[1], bins = n_bins, label = r'SMD $\sigma$ = 2 $\mu$W', alpha=0.9, color = 'green')
                # plt.hist(LDC_Long-LDC_avg_p+SMD_avg_p, bins = n_bins, label = r'LDC210C $\sigma$ = 1 $\mu$W', alpha=0.65, color = 'red' )
                plt.hist(K2602_Long[1]-K2602_avg_p+SMD_avg_p, bins = n_bins, label = r'K2602 $\sigma$ = 3 $\mu$W', alpha=0.4, color = 'blue' )
                plt.xlim(xmin=3.573, xmax = 3.586)
                plt.xlabel('Optical Power ( mW )', fontsize = 14)
                plt.ylabel('Counts', fontsize = 14)
                plt.legend(loc = 'best')
                plt.savefig('Power_Hist')
                plt.show()            
                plt.clf()
                plt.cla()
                plt.close()
            
        PLOT_LIV = False
        if PLOT_LIV:
            SMD_LIV = numpy.loadtxt("Laser_LIV_Data_IBM4_T_25C.txt", delimiter = '\t', unpack = True)
            K2602_LIV = numpy.loadtxt("Laser_LIV_Data_K2602_T_25C.txt", delimiter = '\t', unpack = True)
            
            # What exactly is the difference in voltage at I = 75 ( mA )

            # make a plot of the LIV data
            args = Plotting.plot_arg_multiple()
            
            args.loud = False
            args.x_label = 'Current ( mA )'
            args.y_label = 'Voltage ( V )'
            args.y_label_2 = 'Power ( mW )'

            args.fig_name = 'K2602_LIV'            
            Plotting.plot_two_y_axis_sameX(K2602_LIV[0], K2602_LIV[1], K2602_LIV[2], args)
            
            args.fig_name = 'SMD_LIV'            
            Plotting.plot_two_y_axis_sameX(SMD_LIV[0], SMD_LIV[1], SMD_LIV[2], args)
            
            # Plot the voltages together
            hv_data = []; labels = []; marks = []; 
            hv_data.append([K2602_LIV[0], K2602_LIV[1]]); labels.append('K2602'); marks.append(Plotting.labs_lins[0])
            hv_data.append([SMD_LIV[0], SMD_LIV[1]]); labels.append('SMD'); marks.append(Plotting.labs_lins[1])
            
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.fig_name = 'SMD_K2602_Voltage'
            Plotting.plot_multiple_curves(hv_data, args)
            del hv_data; 
    
            hv_data = []; 
            hv_data.append([K2602_LIV[0], K2602_LIV[2]]);
            hv_data.append([SMD_LIV[0], SMD_LIV[2]]);
            
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.y_label = 'Power ( mW )'
            args.fig_name = 'SMD_K2602_Power'
            Plotting.plot_multiple_curves(hv_data, args)
            del hv_data; 
            
            # Make a plot of the difference in measured power and voltage values         
            delta_v = 1000*(SMD_LIV[1] - K2602_LIV[1])
            delta_p = K2602_LIV[2] - SMD_LIV[2]
                        
            args.loud = True
            args.y_label = 'Voltage ( mV )'
            args.y_label_2 = 'Power ( mW )'
            args.fig_name = 'K2602_SMD_Diff'            
            Plotting.plot_two_y_axis_sameX(K2602_LIV[0][1:], delta_v[1:], delta_p[1:], args)
            
        PLOT_ISRC_CAL = False
        if PLOT_ISRC_CAL:
            Isrc_cal_10 = numpy.loadtxt('Isrc_Test_AD8227_RG_10.txt',skiprows = 1, unpack = True, delimiter = '\t')
            Isrc_cal_12 = numpy.loadtxt('Isrc_Test_AD8227_RG_12.txt',skiprows = 1, unpack = True, delimiter = '\t')
            Isrc_cal_15 = numpy.loadtxt('Isrc_Test_AD8227_RG_15.txt',skiprows = 1, unpack = True, delimiter = '\t')
            Isrc_smd_12 = numpy.loadtxt('Isrc_Test_SMD_RG_12.txt',skiprows = 1, unpack = True, delimiter = '\t')
            
            # Make a plot of the Gain Resistor Optimisation Data
            hv_data = []; labels = []; marks = []; 
    
            hv_data.append([Isrc_cal_15[0], Isrc_cal_15[5]]); labels.append(r'TH R$_{G}$ = 15 k$\Omega$, m = 96.65 $(k\Omega)^{-1}$'); marks.append(Plotting.labs[0]); 
            hv_data.append([Isrc_cal_12[0], Isrc_cal_12[5]]); labels.append(r'TH R$_{G}$ = 12 k$\Omega$, m = 84.08 $(k\Omega)^{-1}$'); marks.append(Plotting.labs[1]); 
            hv_data.append([Isrc_cal_10[0], Isrc_cal_10[5]]); labels.append(r'TH R$_{G}$ = 10 k$\Omega$, m = 75.83 $(k\Omega)^{-1}$'); marks.append(Plotting.labs[2]); 
            hv_data.append([Isrc_smd_12[0], Isrc_smd_12[1]]); labels.append(r'SMD R$_{G}$ = 12 k$\Omega$, m = 87.09 $(k\Omega)^{-1}$'); marks.append(Plotting.labs[3]); 
    
            args = Plotting.plot_arg_multiple()
            
            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = r'Input Voltage $V_{in}$ ( V )'
            args.y_label = r'Sense Current $I_{s}$ ( mA )'
            args.plt_range = [0, 4, 0, 350]
            args.fig_name = 'Isrc_Cal_Data'
            
            Plotting.plot_multiple_curves(hv_data, args)
            
        PLOT_ISRC_VLIM = True
        if PLOT_ISRC_VLIM:
            Isrc_vlim_3 = numpy.loadtxt('Isrc_Test_SMD_RG_12_Vlim_3.txt',skiprows = 1, unpack = True, delimiter = '\t')
            Isrc_vlim_2 = numpy.loadtxt('Isrc_Test_SMD_RG_12_Vlim_2.txt',skiprows = 1, unpack = True, delimiter = '\t')
            Isrc_vlim_1 = numpy.loadtxt('Isrc_Test_SMD_RG_12_Vlim_1.txt',skiprows = 1, unpack = True, delimiter = '\t')
            
            # Make a plot of the Gain Resistor Optimisation Data
            hv_data = []; labels = []; marks = []; 
    
            hv_data.append([Isrc_vlim_3[0], Isrc_vlim_3[1]]); labels.append(r'V$_{lim}$ = 3 ( V )'); marks.append(Plotting.labs[0]); 
            hv_data.append([Isrc_vlim_2[0], Isrc_vlim_2[1]]); labels.append(r'V$_{lim}$ = 2 ( V )'); marks.append(Plotting.labs[1]); 
            hv_data.append([Isrc_vlim_1[0], Isrc_vlim_1[1]]); labels.append(r'V$_{lim}$ = 1 ( V )'); marks.append(Plotting.labs[2]); 
    
            args = Plotting.plot_arg_multiple()
            
            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = r'Input Voltage $V_{in}$ ( V )'
            args.y_label = r'Sense Current $I_{s}$ ( mA )'
            args.plt_range = [0, 3.1, 0, 270]
            args.fig_name = 'Isrc_Vlim_Data'
            
            Plotting.plot_multiple_curves(hv_data, args)          

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def uHeater_Design():
    # Make the plots for the PI Poster 2025
    # R. Sheehan 21 - 8 - 2025
    
    FUNC_NAME = ".uHeater_Design()"
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME
    
    try:
        DATA_HOME = 'c:/users/robertsheehan/Research/Electronics/uHeater_Control/';
        #DATA_HOME = 'E:/Research/Electronics/uHeater_Control/';
        #DATA_HOME = 'D:/Rob/Research/Electronics/uHeater_Control/';
    
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())
            
            PLOT_PWM_AMP = False
            if PLOT_PWM_AMP:
                # Plot the basic measured PWM - DC output and PWM - Amp output
                DClevel = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                FiltLevel = [0.00, 0.32, 0.64, 0.97, 1.30, 1.63, 1.96, 2.29, 2.63, 2.96, 3.29]
                AmpLevel = [0.00, 0.52, 1.06, 1.61, 2.16, 2.71, 3.27, 3.83, 4.39, 4.95, 5.51]
                
                hv_data = []; labels = []; marks = []; 
                hv_data.append([DClevel, AmpLevel]); labels.append('Amplified PWM'); marks.append(Plotting.labs[1]);
                hv_data.append([DClevel, FiltLevel]); labels.append('Filtered PWM'); marks.append(Plotting.labs[0]);  
        
                args = Plotting.plot_arg_multiple()
                
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'PWM Duty Cycle  ( % )'
                args.y_label = 'Measured Voltage ( V )'
                args.plt_range = [0, 105, 0, 6]
                args.fig_name = 'PWM_AO_Demo'
                
                Plotting.plot_multiple_linear_fit_curves(hv_data, args)
                
                del hv_data; del labels; del args; del marks; 
                
            PLOT_PWM_CURR = False
            if PLOT_PWM_CURR:
                # Plot the measured current across different known loads when the PWM AMP output is applied
                
                volts = [0.00, 0.52, 1.06, 1.61, 2.16, 2.71, 3.27, 3.83, 4.39, 4.95, 5.51]
                I500 = [0.00, 1.03, 2.09, 3.18, 4.26, 5.35, 6.45, 7.55, 8.66, 9.76, 10.87]
                I270 = [0.00, 1.95, 3.98, 6.05, 8.12, 10.19, 12.29, 14.40, 16.50, 18.61, 20.71]
                I150 = [0.00, 3.54, 7.21, 10.95, 14.69, 18.44, 22.24, 26.05, 29.86, 33.67, 37.48]
                I055 = [0.00, 9.40, 19.17, 29.11, 39.06, 49.01, 59.13, 69.08, 79.20, 89.51, 99.64]
                I010 = [0.00, 52.26, 106.53, 160.80, 216.08]
                
                hv_data = []; labels = []; marks = []; 
                hv_data.append([volts[0:5], I010]); labels.append(r'R$_{load}$ = 0.01 ( k$\Omega$ )'); marks.append(Plotting.labs[0])
                hv_data.append([volts, I055]); labels.append(r'R$_{load}$ = 0.06 ( k$\Omega$ )'); marks.append(Plotting.labs[1])
                hv_data.append([volts, I150]); labels.append(r'R$_{load}$ = 0.15 ( k$\Omega$ )'); marks.append(Plotting.labs[0])
                hv_data.append([volts, I270]); labels.append(r'R$_{load}$ = 0.27 ( k$\Omega$ )'); marks.append(Plotting.labs[0])
                hv_data.append([volts, I500]); labels.append(r'R$_{load}$ = 0.51 ( k$\Omega$ )'); marks.append(Plotting.labs[0])
                
                args = Plotting.plot_arg_multiple()
                
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Voltage Output ( V )'
                args.y_label = 'Current ( mA )'
                args.plt_range = [0, 6, 0, 225]
                args.fig_name = 'PWM_AO_Current'
                
                Plotting.plot_multiple_linear_fit_curves(hv_data, args)
                
                del hv_data; del labels; del args; del marks;

            COMP_AVG_CAL = False
            if COMP_AVG_CAL:
                # Compute the average of all the calibration curve fit parameters
                
                #filename = r'Calibration_Data\PWM_DC_AMP_Fit_Parameters.txt'
                #filename = r'Calibration_Data_RC_Filt_R_1_C_100\PWM_DC_AMP_Fit_Parameters.txt'
                #filename = r'Calibration_Data_RC_R_10_C_10\PWM_RC_DC_AMP_Fit_Parameters.txt'
                filename = r'Calibration_Data_T_Filt_R_10_C_10\PWM_T_DC_AMP_Fit_Parameters.txt'
    
                if glob.glob(filename):
                    theData = numpy.loadtxt(filename, unpack = True, delimiter = ',',skiprows = 1, usecols=(1, 2, 3, 4))
                
                    # Is the cal curve for D13 actually that different? 
                    # Yes the value computed from D13 is sufficiently different 17 (mV)
                    # to warrant it's being treated differently
        
                    stop = len(theData[0]) - 1

                    m1 = numpy.mean(theData[0][0:stop]); c1 = numpy.mean(theData[1][0:stop]); # PWM Calibration Excluding D13
                    #m2 = numpy.mean(theData[0]); c2 = numpy.mean(theData[1]); # PWM Calibration Including D13
                    #m22 = numpy.mean(theData[0][stop:stop+2]); c22 = numpy.mean(theData[1][stop:stop+2]); # PWM Calibration D13 Only
                    
                    print(theData[0][stop:stop+2])

                    m3 = numpy.mean(theData[2][0:stop]); c3 = numpy.mean(theData[3][0:stop]); # Amp Calibration Excluding D13
                    #m4 = numpy.mean(theData[2]); c4 = numpy.mean(theData[3]); # Amp Calibration Including D13
                    #m44 = numpy.mean(theData[2][stop:stop+2]); c44 = numpy.mean(theData[3][stop:stop+2]); # PWM Calibration D13 Only
        
                    print('\nCalibration Curves Excluding D13')
                    print('Dx PWM Slope:',m1,', Dx PWM Intercept:',c1)
                    print('Dx Amp Slope:',m3,', Dx Amp Intercept:',c3)
                    #print('\nCalibration Curves Including D13')
                    #print('PWM Slope Alt:',m2,', PWM Intercept Alt:',c2)
                    #print('Amp Slope:',m4,', Amp Intercept:',c4) 
                    #print('\nCalibration Curves Only D13')
                    #print('D13 PWM Slope:',m22,', D13 PWM Intercept:',c22)
                    #print('D13 Amp Slope:',m44,', D13 Amp Intercept:',c44) 
                    
                    # DC = 25
                    # v1 = m1*DC+c1; v2 = m2*DC+c2; pwmErr = math.fabs(v1-v2); 
                    # v3 = m3*DC+c3; v4 = m4*DC+c4; ampErr = math.fabs(v3-v4);         
                    # print('\nDC: %(v0)d, PWM val: %(v1)0.3f (V), PWM val: %(v2)0.3f (V), Err: %(v3)0.3f (V)'%{"v0":DC,"v1":v1, "v2":v2, "v3":pwmErr})
                    # print('DC: %(v0)d, Amp val: %(v1)0.3f (V), Amp val: %(v2)0.3f (V), Err: %(v3)0.3f (V)'%{"v0":DC,"v1":v3, "v2":v4, "v3":ampErr})
                    
                    # DC = 50
                    # v1 = m1*DC+c1; v2 = m2*DC+c2; pwmErr = math.fabs(v1-v2); 
                    # v3 = m3*DC+c3; v4 = m4*DC+c4; ampErr = math.fabs(v3-v4);         
                    # print('\nDC: %(v0)d, PWM val: %(v1)0.3f (V), PWM val: %(v2)0.3f (V), Err: %(v3)0.3f (V)'%{"v0":DC,"v1":v1, "v2":v2, "v3":pwmErr})
                    # print('DC: %(v0)d, Amp val: %(v1)0.3f (V), Amp val: %(v2)0.3f (V), Err: %(v3)0.3f (V)'%{"v0":DC,"v1":v3, "v2":v4, "v3":ampErr})
                    
                    # DC = 75
                    # v1 = m1*DC+c1; v2 = m2*DC+c2; pwmErr = math.fabs(v1-v2); 
                    # v3 = m3*DC+c3; v4 = m4*DC+c4; ampErr = math.fabs(v3-v4);         
                    # print('\nDC: %(v0)d, PWM val: %(v1)0.3f (V), PWM val: %(v2)0.3f (V), Err: %(v3)0.3f (V)'%{"v0":DC,"v1":v1, "v2":v2, "v3":pwmErr})
                    # print('DC: %(v0)d, Amp val: %(v1)0.3f (V), Amp val: %(v2)0.3f (V), Err: %(v3)0.3f (V)'%{"v0":DC,"v1":v3, "v2":v4, "v3":ampErr})
                    
            PLOT_CAL_CURVES = False
            if PLOT_CAL_CURVES:
                # Make a plot of the PWM - Amp Output Calibration Curves
                
                d9 = r'Calibration_Data\D9_PWM_Filt_Amp_Data.txt'
                d13 = r'Calibration_Data\D13_PWM_Filt_Amp_Data.txt'
                
                if glob.glob(d9) and glob.glob(d13):
                    data9 = numpy.loadtxt(d9, delimiter = '\t', unpack = True)
                    data13 = numpy.loadtxt(d9, delimiter = '\t', unpack = True)
                    
                    hv_data = []; labels = []; marks = []; 
                    hv_data.append([data9[0], data9[3], data9[4] ]); labels.append(r'D$_{x}$'); marks.append(Plotting.labs[1]);
                    hv_data.append([data13[0], data13[3], data13[4] ]); labels.append(r'D$_{13}$'); marks.append(Plotting.labs[0]);  
        
                    args = Plotting.plot_arg_multiple()
                
                    args.loud = False
                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'PWM Duty Cycle  ( % )'
                    args.y_label = 'Measured Voltage ( V )'
                    args.plt_range = [0, 105, 0, 6]
                    args.fig_name = 'AO_Cal_Curves'
                
                    Plotting.plot_multiple_linear_fit_curves(hv_data, args)
                    
                    del hv_data; del labels; del marks;
                
                    args = Plotting.plot_arg_single()
                    
                    args.loud = True
                    args.curve_label = r'D$_{x}$'
                    args.marker = Plotting.labs[1]
                    args.x_label = 'PWM Duty Cycle  ( % )'
                    args.y_label = 'Measured Voltage ( V )'
                    args.plt_range = [0, 105, 0, 6]
                    args.fig_name = 'AO_Cal_Curve_Dx'
                    
                    Plotting.plot_single_linear_fit_curve_with_errors(data9[0], data9[3], data9[4], args)

                    del args;
        
            PLOT_VARIATIONS = False
            if PLOT_VARIATIONS:
                # Analyse the measured variations in the voltage readings
                # Plot them as a distribution
                # Is variation higher at higher ouputs? 
                
                vals = [0, 1, 7, 9, 10, 11, 12, 13]
                dX = r'Calibration_Data_RC_Filt_R_1_C_100\D%(v1)d_PWM_Filt_Amp_Data.txt'
                #vals = numpy.arange(1, 9, 1)
                #dX = r'Calibration_Data_Pi_Filt_R_10_C_10\D%(v1)d_PWM_Pi_Filt_Amp_Data.txt'
                #dX = r'Calibration_Data_RC_R_10_C_10\D%(v1)d_PWM_RC_Filt_Amp_Data.txt'
                #dX = r'Calibration_Data_T_Filt_R_10_C_10\D%(v1)d_PWM_T_Filt_Amp_Data.txt'
                hv_data = []; labels = []; marks = [];
                variation_data = numpy.array([]) # instantiate an empty numpy array to store all the variation data
                for i in range(0, len(vals), 1):
                    filename = dX%{"v1":vals[i]}
                    if glob.glob(filename):
                        # read the data into memory
                        data = numpy.loadtxt(filename, delimiter = '\t', unpack = True, usecols = (0, 4) )
                        var_data = 1000.0*data[1]
                        
                        # join all the variation data together into a single array
                        variation_data = numpy.append(variation_data, var_data) 
                        
                        # combine all the data together separately
                        hv_data.append([ data[0], var_data ]); 
                        labels.append(r'D$_{ %(v1)d }$'%{ "v1":vals[i] } ); 
                        marks.append( Plotting.labs_pts[ i % len( Plotting.labs_pts ) ] )
                        
                        print('D_%(v1)d: len = %(v4)d, mean = %(v2)0.2f, stdev. = %(v3)0.2f'%{ "v1":vals[i], "v2":numpy.mean(var_data), "v3":numpy.std(var_data, ddof = 1), "v4":len(var_data) } )

                # Compute the mean over all the variation values
                # Make a plot of the distributions        
                variation_data_mean = numpy.mean(variation_data)
                variation_data_sig = numpy.std(variation_data, ddof = 1)        
                print('D_X: len = %(v4)d, mean = %(v2)0.2f, stdev. = %(v3)0.2f'%{ "v1":vals[i], 
                                                                                 "v2":variation_data_mean, 
                                                                                 "v3":variation_data_sig, 
                                                                                 "v4":len(variation_data) } )
                
                # Scale the data for zero mean and unity sigma
                variation_data_mean = numpy.mean(variation_data)
                variation_data_sig = numpy.std(variation_data, ddof = 1)
                scl_variation_data = (variation_data - variation_data_mean) / variation_data_sig
                # Use Sturges' Rule to compute the no. of bins required
                n_bins = int( 1.0 + 3.322*math.log( len(variation_data) ) )
                n_bins = n_bins - 3
                
                plt.hist(scl_variation_data, bins = n_bins, label = r'$\mu$ = %(v1)0.1f ( mV ), $\sigma$ = %(v2)0.1f ( mV )'%{"v1":variation_data_mean, "v2":variation_data_sig}, alpha=0.9, color = 'red', edgecolor = 'black', linestyle = '-')
               
                plt.xlim(xmin=-3, xmax = 3)
                plt.xlabel(r'Scaled Measurements $( \Delta V_{i} - \mu ) / \sigma$', fontsize = 14)
                plt.ylabel('Counts', fontsize = 14)
                plt.legend(loc = 'best')
                plt.savefig('Scaled_Variation_Data')
                plt.show()            
                plt.clf()
                plt.cla()
                plt.close()
                
                # Make a plot of all the error data
                args = Plotting.plot_arg_multiple()
                
                args.loud = False
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'PWM Duty Cycle  ( % )'
                args.y_label = 'Measured Voltage Variation ( mV )'
                args.plt_range = [0, 105, 0, 35]
                args.fig_name = 'Measured_Voltage_Variation_Zm'
                
                #Plotting.plot_multiple_curves(hv_data, args)
                Plotting.plot_multiple_linear_fit_curves(hv_data, args)

            LONG_TIME_MEAS = True
            if LONG_TIME_MEAS:
                # Make plots of the tests with the Decoupling capacitors
                SUB_DIR = 'Decoup_Cap_Test/'
                if os.path.isdir(DATA_HOME):
                    os.chdir(SUB_DIR)
                    print(os.getcwd())

                    # Examine Effect of Decoupling capacitor on Input Supply Voltage
                    # Examine if uHeat output is stable over long-time, Tmeas = 60mins with measurements every 30s
                    # Used NI-DAQ 6001 to measure differential voltages wrt common ground, SR = 5kHz, Nsmpls = 5k
                    INPUT_PLOTS = True
                    if INPUT_PLOTS:
                        # In this case the data stored in the file is a measurement of a voltage across a known load at fixed value
                        # Rload = 0.506 kOhm, Vcc = +7.1V
                        # col0 = PWM0, with pwm level = 50 => Vset ~ 2.72 V
                        # col1 = PWM1, with pwm level = 50 => Vset ~ 2.72 V
                        # col2 = PWM7, with pwm level = 50 => Vset ~ 2.72 V
                        # col3 = External Power Supply with level Vset ~ 2.72 V
                        thefiles = ['AI_DC_Meas_Dev1_ai03_Tmeas_60_Nmeas_120_Cin_None.txt', 
                                    'AI_DC_Meas_Dev1_ai03_Tmeas_60_Nmeas_120_Cin_01.txt', 
                                    'AI_DC_Meas_Dev1_ai03_Tmeas_60_Nmeas_120_Cin_10.txt', 
                                    'AI_DC_Meas_Dev1_ai03_Tmeas_60_Nmeas_120_Cin_100.txt']

                        cap_vals = [0.0, 0.1, 1.0, 10.0] # list of capacitor values used in the measurement, units of uF

                        qnttes = ['PWM0', 'PWM1', 'PWM7', 'CPS'] # quantities being measured

                        Tmeas = 60 # Total measurement time in units of minutes
                        Vmin = 2.720
                        Vmax = 2.745
                        dT = 0.5 # time interval between measurements in units of minutes

                        count = 0
                        for f in thefiles:
                            if glob.glob(f):
                                data = numpy.loadtxt(f, delimiter = ',', unpack = True)

                                # print some statistics
                                # save the descriptors for scaling hist calc later
                                ai_no_ch = len(data) # No. NI-DAQ channels used to perform the measurement
                                avg_arr = numpy.zeros(ai_no_ch)
                                stdev_arr = numpy.zeros(ai_no_ch)
                                print("Statistics for",f)
                                for i in range(0, ai_no_ch, 1):
                                    avg = numpy.mean(data[i])
                                    stdev = numpy.std(data[i], ddof = 1)
                                    avg_arr[i] = avg
                                    stdev_arr[i] = stdev
                                    print('%(v1)s: %(v2)0.4f +/- %(v3)0.4f ( V )'%{"v1":qnttes[i], "v2":avg, "v3":stdev})

                                SHOW_BP = False
                                if SHOW_BP:
                                    # make a box-plot for the data in the file
                                    df = pandas.DataFrame(numpy.transpose(data), columns=qnttes)
                                    boxplot = df.boxplot(column=qnttes)
                                    boxplot.set_ylabel('Measured Voltage ( V )')
                                    boxplot.plot()
                                    plt.title(r'Input Cap = %(v1)0.1f ( $\mu$F )'%{"v1":cap_vals[count]})
                                    plt.ylim(Vmin, Vmax)
                                    plt.savefig(f.replace('.txt','') + '_box')
                                    plt.show()

                                SHOW_HIST = False
                                if SHOW_HIST:
                                    # Make a plot of the scaled histogram of the measured data

                                    # Use Sturges' Rule to compute the no. of bins required
                                    n_bins = int( 1.0 + 3.322*math.log( len(data[0]) ) )
                                    #n_bins = 200

                                    # scale the data to zero mean and unity std. dev. 
                                    for i in range(0, ai_no_ch, 1):
                                        data[i] = (data[i] - avg_arr[i]) / stdev_arr[i]

                                    # plt.hist(SMD_scl_data, bins = n_bins, label = r'SMD $\sigma$ = 2 $\mu$W', alpha=0.9, color = 'red', edgecolor = 'black', linestyle = '-')
                                    # #plt.hist(LDC_scl_data, bins = n_bins, label = r'LDC210C $\sigma$ = 1 $\mu$W', alpha=0.65, color = 'red' , edgecolor = 'black', linestyle = '--')
                                    # plt.hist(K2602_scl_data, bins = n_bins, label = r'K2602 $\sigma$ = 3 $\mu$W', alpha=0.6, color = 'green', edgecolor = 'black', linestyle = ':' )
                                    
                                    for i in range(0, len(data), 1):
                                        plt.hist(data[i], bins = n_bins, label = r'%(v1)s'%{"v1":qnttes[i]}, 
                                                 alpha=0.9, color = Plotting.colours[i], edgecolor = 'black', linestyle = '-')

                                    plt.xlim(xmin=-4, xmax = 4)
                                    #plt.xlim(xmin=2.71, xmax = 2.75)
                                    plt.ylim(ymin=0, ymax = 600e+3)
                                    plt.xlabel(r'Scaled Measurements $( V_{i} - \mu ) / \sigma$', fontsize = 14)
                                    plt.ylabel('Counts', fontsize = 14)
                                    plt.legend(loc = 'best')
                                    plt.title(r'Input Cap = %(v1)0.1f ( $\mu$F )'%{"v1":cap_vals[count]})
                                    plt.savefig(f.replace('.txt','') + '_hist')
                                    #plt.show()            
                                    plt.clf()
                                    plt.cla()
                                    plt.close()

                                SHOW_TIME_SER = True
                                if SHOW_TIME_SER:
                                    # Make a plot of the averaged measurements over time
                                    # No need to include std. dev. as error bar since it is so small < 1mV
                                    # Is there a correlation between meas. val and time? 
                                    # Is there a drift in meas. val over time
                                    
                                    # Compute averages on sub-sets of the measured data
                                    # similar to how the data was measured in any case
                                    no_meas = 120 # No. meas. performed 
                                    no_smpls = 4999 # compute the average meas. val. every n_smpls
                                    
                                    avg_vals = numpy.zeros((no_meas, ai_no_ch))
                                    times = numpy.arange(0, Tmeas, dT)
                                    hv_data = []
                                    marks = []
                                    for i in range(0, ai_no_ch, 1):
                                        for j in range(0, no_meas, 1):
                                            start = j*no_smpls
                                            end = start + no_smpls
                                            avg = numpy.mean(data[i][start:end])
                                            avg_vals[j][i] = avg
                                        hv_data.append([times, avg_vals[:,i]])
                                        marks.append(Plotting.labs_lins[i])
                                        
                                        # Compute the averages of the data and examine whether or not they are correlated with time
                                        savg = numpy.mean(avg_vals[:,i])
                                        sstdev = numpy.std(avg_vals[:,i], ddof = 1)
                                        # Pearson-r doesn't make sense in this case
                                        # pearson_r = numpy.corrcoef(times, avg_vals[:,i])
                                        lincoeffs = Common.linear_fit(times, avg_vals[:,i], [1,1])
                                        print("%(v1)s: %(v2)0.4f +/- %(v3)0.4f (V), m = %(v4)0.2f ( uV / min ), c = %(v5)0.4f ( V )"%{"v1":qnttes[i], "v2":savg,"v3":sstdev,"v4":1.0e+6*lincoeffs[1],"v5":lincoeffs[0]})

                                    PLOT_TIME_SER = True
                                    if PLOT_TIME_SER:
                                        # Make a time-series plot of the averaged data
                                        args = Plotting.plot_arg_multiple()

                                        args.loud = False
                                        args.crv_lab_list = qnttes
                                        args.mrk_list = marks
                                        args.x_label = 'Time ( mins )'
                                        args.y_label = 'Voltage ( V )'
                                        args.plt_range = [0, Tmeas, Vmin, Vmax]
                                        args.plt_title = r'Input Cap = %(v1)0.1f ( $\mu$F )'%{"v1":cap_vals[count]} 
                                        args.fig_name = f.replace('.txt','') + '_time'

                                        Plotting.plot_multiple_curves(hv_data, args)

                                    del avg_vals; del hv_data; del marks; 

                                count += 1

                                del data; del avg_arr; del stdev_arr; 

                    # Effect of Decoupling capacitor on Output Voltage Value
                    OUTPUT_PLOTS = False
                    if OUTPUT_PLOTS:
                        pass
                else:
                    ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate directory:' + SUB_DIR
                    raise Exception

        else:
            ERR_STATEMENT = ERR_STATEMENT + '\nCannot locate directory:' + DATA_HOME
            raise Exception
        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Combine_Avg_Std():

    # Combine several averages and std. deviations into a single value
    # Suppose you have several measurements of the same quantity obtained at different times
    # Is it possible to compute a single average and a single std. deviation from avg and std
    # from all previous measurements? Yes, it is provided you know the no. samples used to compute
    # each previous avg and std. dev. s
    # for more information consult the following
    # https://stats.stackexchange.com/questions/55999/is-it-possible-to-find-the-combined-standard-deviation?noredirect=1&lq=1
    # https://stats.stackexchange.com/questions/43031/how-to-prove-that-averaging-averages-of-different-partitions-of-a-dataset-produc
    # https://stats.stackexchange.com/questions/10441/how-to-calculate-the-variance-of-a-partition-of-variables?noredirect=1&lq=1
    # R. Sheehan 28 - 1 - 2026

    # Here is some sample data with different no. of samples
    avg_arr = numpy.array([2.4, 2.0, 2.3, 2.1])
    stdev_arr = numpy.array([0.8, 1.2, 0.9, 1.1])
    counts_arr = numpy.array([10, 5, 7, 9])

    # Here is how to compute the combined statistics    
    avg_combined, std_combined = Combine_Statistics(avg_arr, stdev_arr, counts_arr, equal_sample_sizes = False)
    print("Combined statistics for unequal sample size data sets")
    print("ai%(v1)d: %(v2)0.4f +/- %(v3)0.4f (V)"%{"v1":0, "v2":avg_combined, "v3":std_combined})

    # Let's take a look at a calculation in which the sample sizes are all equal
    # Here is some sample data with equal sample sizes
    avg_arr = numpy.array([2.4, 2.0, 2.3, 2.1])
    stdev_arr = numpy.array([0.8, 1.2, 0.9, 1.1])
    counts_arr = numpy.array([9, 9, 9, 9])

    # Here is how to compute the combined statistics
    avg_combined, std_combined = Combine_Statistics(avg_arr, stdev_arr, counts_arr, equal_sample_sizes = False)
    print("\nCombined statistics for equal sample size data sets")
    print("ai%(v1)d: %(v2)0.4f +/- %(v3)0.4f (V)"%{"v1":0, "v2":avg_combined, "v3":std_combined})

    avg_combined, std_combined = Combine_Statistics(avg_arr, stdev_arr, counts_arr, equal_sample_sizes = True)
    print("ai%(v1)d: %(v2)0.4f +/- %(v3)0.4f (V)"%{"v1":0, "v2":avg_combined, "v3":std_combined})
    print()

def Combine_Statistics(avg_arr, stdev_arr, counts_arr, equal_sample_sizes = True, loud = False):

    """
    Combine averages and standard deviations from multiple different measurements into a single value
    Account for unequal sample sizes if necessary

    Input:
        avg_arr: numpy array of floats giving averages from different measurements
        stdev_arr: numpy array of floats giving std. dev. from different measurements
        count_arr: numpy array of ints giving sample size for each measurement

    Output:
        avg_combined, std_combined

    R. Sheehan 28 - 1 - 2026
    """

    # Is it possible to compute a single average and a single std. deviation from avg and std
    # from all previous measurements? Yes, it is provided you know the no. samples used to compute
    # each previous avg and std. dev. s
    # for more information consult the following
    # https://stats.stackexchange.com/questions/55999/is-it-possible-to-find-the-combined-standard-deviation?noredirect=1&lq=1
    # https://stats.stackexchange.com/questions/43031/how-to-prove-that-averaging-averages-of-different-partitions-of-a-dataset-produc
    # https://stats.stackexchange.com/questions/10441/how-to-calculate-the-variance-of-a-partition-of-variables?noredirect=1&lq=1

    FUNC_NAME = ".Combine_Statistics()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if len(avg_arr) > 0 else False
        c2 = True if len(stdev_arr) > 0 else False
        c3 = True if len(counts_arr) > 0 else False
        c4 = True if len(counts_arr) == len(stdev_arr) else False
        c5 = True if len(counts_arr) == len(avg_arr) else False
        c10 = c1 and c2 and c3 and c4 and c5

        if c10:
            avg_combined = numpy.average(avg_arr) if equal_sample_sizes else numpy.average(avg_arr, weights=counts_arr)
            numer = denom = 0.0
            denom = numpy.sum(counts_arr) - 1
            for i in range(0, len(stdev_arr), 1):
                numer += (counts_arr[i] - 1)*stdev_arr[i]**2 + counts_arr[i]*(avg_arr[i] - avg_combined)**2
            std_combined = math.sqrt(numer / denom)
            if loud:
                print()
                print("Combined Value: %(v2)0.4f +/- %(v3)0.4f (V)"%{"v2":avg_combined, "v3":std_combined})
            return avg_combined, std_combined
        else:
            if c1 is False: ERR_STATEMENT = ERR_STATEMENT + '\nNo data contained in avg_arr'
            if c2 is False: ERR_STATEMENT = ERR_STATEMENT + '\nNo data contained in stdev_arr'
            if c3 is False or c4 is False or c5 is False: ERR_STATEMENT = ERR_STATEMENT + '\nInput arrays are not correctly sized'            
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

