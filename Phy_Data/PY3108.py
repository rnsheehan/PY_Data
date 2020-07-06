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

MOD_NAME_STR = "PY3108"

def CE_AMP_IV_Char(Vcc, Vb, Rc, Rb, Rbval, ratio, loud = False):
    
    # make plots of measured IV characteristic of npn-BJT CE amplifier
    # make a plot of measured Ic versus Vce for various Vb
    # include load line on plot
    # R. Sheehan 6 - 7 - 2020

    FUNC_NAME = ".CE_AMP_IV_Char()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/Robert/Teaching/PY3108/Data/npn_BJT/CE_IV_Char/"

        os.chdir(DATA_HOME)

        print(os.getcwd())        

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 
        for i in range(0, len(Vb), 1):
            filename = "Ichar_Vext_%(v0)d_Vb_%(v3)s_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v0":Vcc, "v1":Rc, "v2":Rb, "v3":str(Vb[i]).replace(".","")}    
            if glob.glob(filename):
                if loud: 
                    print(filename)
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                hv_data.append([data[2], data[1]])
                labels.append('$I_{b}$ = %(v1)0.1f $\mu$A'%{"v1":1000.0*(Vb[i] / Rbval)})
                marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] )
            count = count + 1 

        # Add Load Line
        Icc = Vcc / (Rbval / ratio)
        hv_data.append([[0.0, Vcc],[Vcc / (Rbval / ratio), 0.0]])
        labels.append('Load Line')
        marks.append(Plotting.labs_line_only[1])

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = '$V_{ce}$ / V'
        args.y_label = '$I_{c}$ / mA'
        args.fig_name = "Ichar_Vext_%(v0)d_Rc_%(v1)s_Rb_%(v2)s"%{"v0":Vcc, "v1":Rc, "v2":Rb, }

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Plot_CE_Amp():
    # run the method for plotting the Vgain for various values of Rc, Rb
    # R. Sheehan 6 - 7 - 2020

    FUNC_NAME = ".Plot_CE_Amp()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:        
        # Measured gain for various Vcc
        run_loop = False        
        if run_loop:
            Rc = ["0177", "00344", "0383", "0987", "0986"]; Rb = ["518", "330", "217", "217", "564"]
            for i in range(0, len(Rc), 1):
                CE_AMP_Vgain(Rc[i], Rb[i], vgain = True, loud = True)

        # Comparison for fixed Vcc
        run_loop = False
        if run_loop:
            Rc = ["0383", "0987", "0177", "0986", "00344"]; Rb = ["217", "217", "518", "564", "330"]
            ratios = [5.67, 21.99, 29.3, 57.2, 95.93]
            CE_AMP_Vgain_Compare(Rc, Rb, ratios, vgain = True, loud = True)

        # Plot Measured characteristic
        run_loop = True        
        if run_loop:
            Vcc = 5.0
            Rc = ["0383", "0987", "0177", "0986", "00344"]; Rb = ["217", "217", "518", "564", "330"]
            Rbval = [2.17, 21.99, 5.18, 56.4, 3.3]
            ratios = [5.67, 21.99, 29.3, 57.2, 95.93]
            
            Vb = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
            
            for k in range(0, len(Rbval), 1):
                CE_AMP_IV_Char(Vcc, Vb, Rc[k], Rb[k], Rbval[k], ratios[k], True)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def CE_AMP_Vgain(Rc, Rb, vgain = True, loud = False):
    # make plots of measured voltage gain characteristic of npn-BJT CE amplifier
    # make a plot of measured Vc versus Vin for various Vcc
    # R. Sheehan 6 - 7 - 2020

    FUNC_NAME = ".CE_AMP_Vgain()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/Robert/Teaching/PY3108/Data/npn_BJT/CE_Vgain/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        filename = "Vgain_Vc_*_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v1":Rc, "v2":Rb}

        files = glob.glob(filename)

        if files:
            if loud:
                print("Following files exist: ")
                print(files)

            # import the data
            hv_data = []; labels = []; marks = []; 
            count = 0; 
            for f in files: 
                num_list = Common.extract_values_from_string(f)
                data = numpy.loadtxt(f, delimiter = '\t', unpack = True); 
                if vgain: # plot voltage gain
                    hv_data.append([data[2], data[3]])
                else:  # plot current gain
                    hv_data.append([data[0], data[1]])
                labels.append('$V_{cc}$ = %(v1)s V'%{"v1":num_list[0]})
                marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] )
                count = count + 1 

            # plot the data
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = '$V_{in}$ / V' if vgain else '$I_{in}$ / mA'
            args.y_label = '$V_{out}$ / V' if vgain else '$I_{out}$ / mA'
            args.plt_range = [0, 3, 0, 7]
            num_list = Common.extract_values_from_string(files[0])
            if vgain:
                args.fig_name = files[0].replace("_Vc_%(v1)s"%{"v1":num_list[0]},"").replace(".txt","")
            else:
                args.fig_name = files[0].replace("_Vc_%(v1)s"%{"v1":num_list[0]},"").replace(".txt","").replace("Vgain","Igain")

            Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def CE_AMP_Vgain_Compare(Rc, Rb, ratios, vgain = True, loud = False):
    # make plots of measured voltage gain characteristic of npn-BJT CE amplifier
    # make a plot of measured Vc versus Vin for fixed Vcc and various Rb / Rc
    # R. Sheehan 6 - 7 - 2020

    FUNC_NAME = ".CE_AMP_Vgain_Compare()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/Robert/Teaching/PY3108/Data/npn_BJT/CE_Vgain/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        filename = "Vgain_Vc_5_Rc_*_Rb_*.txt"

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 
        val = 0; 
        for i in range(0, len(ratios), 1): 
            filename = "Vgain_Vc_5_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v1":Rc[i], "v2":Rb[i]}
            if glob.glob(filename):
                num_list = Common.extract_values_from_string(filename)
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                if vgain: # plot voltage gain
                    for j in range(0, len(data[3]), 1):
                        data[3][j] = data[3][j] / data[2][j]
                    hv_data.append([data[2], data[3]])
                else:  # plot current gain
                    hv_data.append([data[0], data[1]])
                labels.append('$R_{b} / R_{c}$ = %(v1)0.2f'%{"v1":ratios[i]})
                marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] )
            count = count + 1

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = '$V_{in}$ / V' if vgain else '$I_{in}$ / mA'
        args.y_label = '$G_{V}$' if vgain else '$G_{I}$'
        args.plt_range = [0, 3, 0, 10]
        if vgain:
            args.fig_name = filename.replace("_Rc_%(v1)s_Rb_%(v2)s"%{"v1":Rc[-1], "v2":Rb[-1]},"").replace(".txt","")
        else:
            args.fig_name = filename.replace("_Rc_%(v1)s_Rb_%(v2)s"%{"v1":Rc[-1], "v2":Rb[-1]},"").replace(".txt","").replace("Vgain","Igain")

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)