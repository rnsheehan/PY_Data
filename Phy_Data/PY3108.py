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
HOME = False
USER = 'Robert' if HOME else 'robertsheehan/OneDrive - University College Cork/Documents'

def CE_AMP_IV_Char(Vcc, Vb, Rc, Rb, Rbval, ratio, loud = False):
    
    # make plots of measured IV characteristic of npn-BJT CE amplifier
    # make a plot of measured Ic versus Vce for various Vb and fixed Vcc
    # include load line on plot
    # R. Sheehan 6 - 7 - 2020

    FUNC_NAME = ".CE_AMP_IV_Char()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/CE_IV_Char/"

        os.chdir(DATA_HOME)

        print(os.getcwd())        

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 
        for i in range(0, len(Vb), 1):
            #filename = "Ichar_Vext_%(v0)d_Vb_%(v3)s_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v0":Vcc, "v1":Rc, "v2":Rb, "v3":str(Vb[i]).replace(".","")}    
            filename = "Ichar_Vext_%(v0)d_Vb_%(v3)s_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v0":Vcc, "v1":Rc, "v2":Rb, "v3":Vb[i]}
            if glob.glob(filename):
                if loud: 
                    print(filename)
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                Ib = numpy.mean(data[2])
                dIb = 0.5*(numpy.max(data[2]) - numpy.min(data[2]))
                hv_data.append([data[5], data[4]])
                #labels.append('$I_{b}$ = %(v1)0.1f $\mu$A'%{"v1":1000.0*(Vb[i] / Rbval)})
                labels.append('$I_{b}$ = %(v1)0.2f $\pm$ %(v2)0.2f mA'%{"v1":Ib, "v2":dIb})
                #labels.append('$V_{b}$ = %(v1)0.1f V'%{"v1":Vb[i]})
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

def EF_AMP_IV_Char(Vcc, Vb, Rc, Rb, Rbval, Rcval, loud = False):
    
    # make plots of measured IV characteristic of npn-BJT EF amplifier
    # make a plot of measured Ic versus Vce for various Vb and fixed Vcc
    # include load line on plot
    # R. Sheehan 8 - 7 - 2020

    FUNC_NAME = ".EF_AMP_IV_Char()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/EF_IV_Char/"

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
                Ib = numpy.mean(data[0])
                dIb = 0.5*(numpy.max(data[0]) - numpy.min(data[0]))
                hv_data.append([data[4], data[3]])
                #labels.append('$V_{b}$ = %(v1)0.2f $\pm$ %(v2)0.2f V'%{"v1":Ib, "v2":dIb})
                labels.append('$V_{b}$ = %(v1)0.1f V'%{"v1":Ib})
                marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] )
            count = count + 1 

        # Add Load Line
        Icc = Vcc / (Rbval + Rcval)
        hv_data.append([[0.0, Vcc],[Icc, 0.0]])
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

def CE_AMP_IV_Char_Compare(Vcc, Vb, Rc, Rb, Rbval, ratio, loud = False):
    
    # make plots of measured IV characteristic of npn-BJT CE amplifier
    # make a plot of measured Ic versus Vce for various Vcc and fixed Vb
    # include load line on plot
    # R. Sheehan 7 - 7 - 2020

    FUNC_NAME = ".CE_AMP_IV_Char_Compar()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/CE_IV_Char/"

        os.chdir(DATA_HOME)

        print(os.getcwd())        

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 
        for i in range(0, len(Vcc), 1):
            filename = "Ichar_Vext_%(v0)d_Vb_%(v3)s_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v0":Vcc[i], "v1":Rc, "v2":Rb, "v3":Vb}    
            if glob.glob(filename):
                if loud: 
                    print(filename)
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                #Ib = numpy.mean(data[1])
                #dIb = 0.5*(numpy.max(data[1]) - numpy.min(data[1]))
                hv_data.append([data[4], data[3]])
                #labels.append('$I_{b}$ = %(v1)0.1f $\mu$A'%{"v1":1000.0*(Vb[i] / Rbval)})
                #labels.append('$I_{b}$ = %(v1)0.2f $\pm$ %(v2)0.2f mA'%{"v1":Ib, "v2":dIb})
                labels.append('$V_{cc}$ = %(v1)0.1f V'%{"v1":Vcc[i]})
                marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] )
            count = count + 1 

        # Add Load Line
        Icc = Vcc[-1] / (Rbval / ratio)
        hv_data.append([[0.0, Vcc[-1]],[Vcc[-1] / (Rbval / ratio), 0.0]])
        labels.append('LL $V_{cc}$ = %(v1)0.1f V'%{"v1":Vcc[-1]})
        marks.append( Plotting.labs_line_only[1] )

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = '$V_{ce}$ / V'
        args.y_label = '$I_{c}$ / mA'
        args.plt_range = [0, 8, 0, 60]
        args.fig_name = "Ichar_Vb_%(v0)s_Rc_%(v1)s_Rb_%(v2)s"%{"v0":Vb, "v1":Rc, "v2":Rb}

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def EF_AMP_IV_Char_Compare(Vcc, Vb, Rc, Rb, Rbval, Rcval, loud = False):
    
    # make plots of measured IV characteristic of npn-BJT Ef amplifier
    # make a plot of measured Ic versus Vce for various Vcc and fixed Vb
    # include load line on plot
    # R. Sheehan 7 - 7 - 2020

    FUNC_NAME = ".EF_AMP_IV_Char_Compar()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/EF_IV_Char/"

        os.chdir(DATA_HOME)

        print(os.getcwd())        

        # import the data
        hv_data = []; labels = []; marks = []; 
        count = 0; 
        for i in range(0, len(Vcc), 1):
            filename = "Ichar_Vext_%(v0)d_Vb_%(v3)s_Rc_%(v1)s_Rb_%(v2)s.txt"%{"v0":Vcc[i], "v1":Rc, "v2":Rb, "v3":Vb}    
            if glob.glob(filename):
                if loud: 
                    print(filename)
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True); 
                #Ib = numpy.mean(data[1])
                #dIb = 0.5*(numpy.max(data[1]) - numpy.min(data[1]))
                hv_data.append([data[4], data[3]])
                #labels.append('$I_{b}$ = %(v1)0.1f $\mu$A'%{"v1":1000.0*(Vb[i] / Rbval)})
                #labels.append('$I_{b}$ = %(v1)0.2f $\pm$ %(v2)0.2f mA'%{"v1":Ib, "v2":dIb})
                labels.append('$V_{cc}$ = %(v1)0.1f V'%{"v1":Vcc[i]})
                marks.append(Plotting.labs_pts[ count%len(Plotting.labs_pts) ] )
            count = count + 1 

        # Add Load Line
        Icc = Vcc[-1] / (Rbval + Rcval)
        hv_data.append([[0.0, Vcc[-1]],[Icc, 0.0]])
        labels.append('LL $V_{cc}$ = %(v1)0.1f V'%{"v1":Vcc[-1]})
        marks.append( Plotting.labs_line_only[1] )

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = '$V_{ce}$ / V'
        args.y_label = '$I_{c}$ / mA'
        args.plt_range = [0, 4, 0, 100]
        args.fig_name = "Ichar_Vb_%(v0)s_Rc_%(v1)s_Rb_%(v2)s"%{"v0":Vb, "v1":Rc, "v2":Rb}

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
            #Rc = ["0177", "00344", "0383", "0987", "0986"]; Rb = ["518", "330", "217", "217", "564"]
            Rc = ["047"]; Rb = ["177"]
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
            #Rc = ["0383", "0987", "0177", "0986", "00344"]; Rb = ["217", "217", "518", "564", "330"]
            #Rbval = [2.17, 21.99, 5.18, 56.4, 3.3]
            #ratios = [5.67, 21.99, 29.3, 57.2, 95.93]            
            #Vb = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

            #Rc = ["0099", "0215", "0341", "0468", "0981", "177"]; Rb = ["0986", "215", "325", "0986", "1779", "387"]
            #Rbval = [0.986, 2.15, 3.25, 0.986, 1.779, 3.87]
            #ratios = [95.59, 100.00, 95.307, 21.07, 18.13, 21.86]            
            #Vb = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

            #for k in range(0, len(Rbval), 1):
            #    CE_AMP_IV_Char(Vcc, Vb, Rc[k], Rb[k], Rbval[k], ratios[k], True)

            Rbval = 0.1; Ratio = 14.92; 
            Rc = "67"; Rb = "100"; Vb = ["085","090","095","100"]
            
            CE_AMP_IV_Char(Vcc, Vb, Rc, Rb, Rbval, Ratio, True)

         # Plot Measured characteristic for EF Amp
        run_loop = False       
        if run_loop:
            Rc = ["0477"]; Rb = ["177"]
            Vcc = [5, 7]; Rbval = 0.177; Rcval = 0.047; 
            Vb = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
            for k in range(0, len(Vcc), 1):
                EF_AMP_IV_Char(Vcc[k], Vb, Rc[0], Rb[0], Rbval, Rcval, True)

        # Plot Measured characteristic for different Vcc
        run_loop = False       
        if run_loop:
            Vcc = [5.0, 7.0, 10.0, 12.0, 15.0]

            Rc = "0477"; Rb = "177"; Rbval = 0.177; Rcval = 0.047; Vb = "10"; 
            
            EF_AMP_IV_Char_Compare(Vcc, Vb, Rc, Rb, Rbval, Rcval, True)                

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
        #DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/CE_IV_Char/"
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/EF_Vgain/"

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
            #args.plt_range = [0, 3, 0, 7]
            num_list = Common.extract_values_from_string(files[0])
            if vgain:
                args.fig_name = files[0].replace("_Vc_%(v1)s"%{"v1":num_list[0]},"").replace(".txt","")
            else:
                args.fig_name = files[0].replace("_Vc_%(v1)s"%{"v1":num_list[0]},"").replace(".txt","").replace("Vgain","Igain")

            Plotting.plot_multiple_curves(hv_data, args)
        else:
            raise Exception

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
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/CE_IV_Char/"

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

def Vbe_Loop():
    # make plot of the measured voltage for the Vbe loop
    # R. Sheehan 8 - 7 - 2020

    FUNC_NAME = ".Vbe_Loop()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/npn_BJT/Base_Loop"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        rvals = ["0177", "0382"]
        R = [0.177, 0.382]

        hv_data = []; labels = []; marks = []; 

        for i in range(0, len(rvals), 1):
            filename = "Vbe_loop_R_%(v0)s.txt"%{"v0":rvals[i]}
            if glob.glob(filename):
                data = numpy.loadtxt(filename, delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[1]])
                labels.append('$R_{e}$ = %(v1)0.3f k$\Omega$'%{"v1":R[i]})
                marks.append(Plotting.labs_pts[i%len(Plotting.labs_pts)])

        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.x_label = '$V_{b}$ / V'
        args.y_label = '$V_{e}$ / V'
        args.crv_lab_list = labels
        args.mrk_list = marks

        Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def OpAmpComparison():

    # plot the data obtained from comparing the different op-amps
    # different op-amps were used to operate a current source
    # some worked correctly, some didn't
    # data is stored in columns of file in the form
    # V_supplied (V) \t Vcontrol (V) \t VR3 (V) \t Vload (V) \t IR3 = Isourced (mA)
    # R. Sheehan 23 - 11 - 2020

    FUNC_NAME = ".Vbe_Loop()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/OpAmpTesting/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        files = glob.glob("*.txt")

        old_target, sys.stdout = sys.stdout, open('Regression_Analysis.txt', 'w')

        print("PY3108 Current Source")
        print("R1 = 55 Ohm, R2 = 10 Ohm, R3 = 5 Ohm, Rload = 10 Ohm")
        print("R2 / (R1 R3) = 36.3636 Ohm^{-1}")
        print("")
        print("filename\tEstimate R2 / (R1 R3)\tEstimate Rload")

        LOUDNESS = False

        for f in files:
            data = numpy.loadtxt(f, delimiter = '\t', unpack = True)
            
            # Make a plot of the measured voltages versus supplied voltage
            hv_data = []; labels = []; marks = []; 
            hv_data.append([data[0], data[1]]); labels.append('$V_{ctrl}$'); marks.append(Plotting.labs_pts[0]); 
            hv_data.append([data[0], data[2]]); labels.append('$V_{R3}$'); marks.append(Plotting.labs_pts[1]); 
            hv_data.append([data[0], data[3]]); labels.append('$V_{load}$'); marks.append(Plotting.labs_pts[2]); 

            args = Plotting.plot_arg_multiple()

            args.loud = LOUDNESS
            args.x_label = 'Supplied Voltage / V'
            args.y_label = 'Measured Voltage / V'
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.fig_name = 'Measured_Voltage' + f.replace('Isrc','').replace('.txt','')

            Plotting.plot_multiple_curves(hv_data, args)

            # Make a plot of sourced current versus supplied voltage

            args = Plotting.plot_arg_single()

            args.loud = LOUDNESS
            args.x_label = 'Supplied Voltage / V'
            args.y_label = 'Sourced Current / mA'
            args.fig_name = 'Sourced_Current' + f.replace('Isrc','').replace('.txt','')

            Plotting.plot_single_linear_fit_curve(data[0], data[4], args)

            # Make a plot of voltage load versus sourced current
            args = Plotting.plot_arg_single()

            args.loud = LOUDNESS
            args.x_label = 'Sourced Current / mA'
            args.y_label = 'Load Voltage / V'
            args.fig_name = 'Load_Voltage' + f.replace('Isrc','').replace('.txt','')

            Plotting.plot_single_linear_fit_curve(data[4], data[3], args)

            # Perform Regression Analysis on the data
            pars1 = Common.linear_fit(data[0], data[4], [0, 1])
            pars2 = Common.linear_fit(data[4], data[3], [0, 1])

            #print(f)
            #print("Estimate R2 / (R1 R3): ", pars1[1], " Ohm^{-1}")
            #print("Estimate Rload: ", 1000.0*pars2[1], " Ohm")
            #print("")
            print(f,"\t",pars1[1],"\t",1000.0*pars2[1])


        sys.stdout = old_target # return to the usual stdout

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def InAmp_Isrc_Char():

    # plot the measured data from the characterisation of the InAmp based current source
    # R. Sheehan 15 - 10 - 2021

    FUNC_NAME = ".InAmp_Isrc_Char()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY3108/Data/Current_Source/Isrc_V2_2021/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())
            
            # Isrc Parameters
            # InAmp INA122PA -> k = 5, R_{int} = 200k, R_{G} = 10k, R_{1} = 0.001k
            k=5.0; Rint = 200.0; Rg = 10.0; R1 = 1.0/1000.0; 
            G = k + Rint/Rg
            Rlist = [5.2, 10.2, 14.9, 21.9]
            files = ['IBM4_V2_R_5p2.txt', 'IBM4_V2_R_10p2.txt', 'IBM4_V2_R_14p9.txt', 'IBM4_V2_R_21p9.txt']

            # read the data
            hv_data = []; labels = []; marks = []; 
            for i in range(0, len(files), 1):
                data = numpy.loadtxt(files[i], delimiter = '\t', unpack = True)
                hv_data.append([data[0], data[2]])
                marks.append(Plotting.labs_pts[i])
                labels.append('R = %(v1)0.1f $\Omega$'%{"v1":Rlist[i]})

            # plot the data
            args = Plotting.plot_arg_multiple()

            args.loud = False
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = '$V_{in}$ / V'
            args.y_label = '$I_{load}$ / mA'
            args.fig_name = 'Isrc_v2_Current_Output'
            args.plt_range = [0, 3.3, 0, 140]

            Plotting.plot_multiple_curves(hv_data, args)

            # Take an average over all the data sets
            Vavg = []; Iavg = []; Verr = []; Ierr = []; 
            N_data = len(hv_data[0][0])
            N_meas = len(hv_data)
            print(N_data)
            for i in range(0, N_data, 1):
                Vsum = 0.0; Isum = 0.0; Vmax = -50.0; Vmin = 50.0; Imax = -500.0; Imin = +500.0; 
                for j in range(0, N_meas, 1):
                    Vsum = Vsum + hv_data[j][0][i]
                    Isum = Isum + hv_data[j][1][i]
                    if hv_data[j][0][i] > Vmax: Vmax = hv_data[j][0][i]
                    if hv_data[j][0][i] < Vmin: Vmin = hv_data[j][0][i]
                    if hv_data[j][1][i] > Imax: Imax = hv_data[j][1][i]
                    if hv_data[j][1][i] < Imin: Imin = hv_data[j][1][i]
                Vsum = Vsum / N_meas
                Isum = Isum / N_meas
                Vavg.append(Vsum)
                Iavg.append(Isum)
                Verr.append(Vmax - Vmin)
                Ierr.append(Imax - Imin)

            # estimate of largest errors
            print("Max{ Verr }: ",max(Verr)*1000, " mV")
            print("Max{ Ierr }: ",max(Ierr), " mA")

            # Make a linear fit to the data set
            pars = Common.linear_fit(numpy.asarray(Vavg), numpy.asarray(Iavg), [0, 1], False)
            print('Linear Fit')
            print('Intercept: ',pars[0])
            print('Slope: ',pars[1])
            print('G R1 Actual: ', G*R1,', G R1 Fit: ',1.0/pars[1])

            # Plot the averaged data
            args = Plotting.plot_arg_single()

            args.loud = True
            args.curve_label = '$I_{load}$ = %(v1)0.3f $V_{in}$ + %(v2)0.3f'%{"v1":pars[1],"v2":pars[0]}
            args.marker = Plotting.labs_pts[0]
            args.x_label = '$V_{in}$ / V'
            args.y_label = '$I_{load}$ / mA'
            args.fig_name = 'Isrc_v2_Average_Current_Output'
            args.plt_range = [0, 3.3, 0, 140]

            #Plotting.plot_single_curve(Vavg, Iavg, args)
            #Plotting.plot_single_linear_fit_curve(Vavg, Iavg, args)
            Plotting.plot_single_linear_fit_curve_with_errors(Vavg, Iavg, Ierr, args)


    except Exception as e:
        print(ERR_STATEMENT)
        print(e)