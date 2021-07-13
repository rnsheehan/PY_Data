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

def AM_Diode_Meas_Compar_1():

    # Plot the measured diode characteristic data
    # data taken from a standard set-up and an AM based set-up
    # R. Sheehan 8 - 7 - 2021

    FUNC_NAME = ".AM_Diode_Meas_Compar()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_Diode_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # the data
        Rd = 0.01; # impedance of resistor used to determine diode current
        Vr_std = [0, 0, 0, 0, 0, 0.004, 0.0256, 0.0727, 0.1306, 0.1983, 0.269, 
                  0.35, 0.427, 0.508, 0.588, 0.678, 0.76, 0.845, 0.929, 1.019, 1.103]; # voltage across diode resistor measured using standard set up
        Vd_std = [0, 0.0922, 0.1895, 0.295, 0.392, 0.487, 0.561, 0.615, 0.649, 0.675, 
                  0.694, 0.708, 0.726, 0.737, 0.747, 0.755, 0.765, 0.772, 0.779, 0.786, 0.791]; # voltage across diode measured using standard set up
        Id_std = []; # current going into diode measured using standard set up
        for i in range(0, len(Vr_std), 1):
            Id_std.append(Vr_std[i] / Rd)

        # make a fit to the data using the diode equation
        T = 25; 
        pars_std = diode_fit(Id_std, Vd_std, T); 

        # generate residual data based on fit
        Vd_std_fit = []
        for i in range(0, len(Id_std), 1):
            Vd_std_fit.append( diode_voltage(Id_std[i], pars_std[0], pars_std[1], T) )

        Vr_AM = [0, 0, 0.0028, 0.0878, 0.176, 0.355, 0.521, 0.72, 0.902]; # voltage across diode resistor measured using AM
        Vd_AM = [0, 0.185, 0.47, 0.617, 0.661, 0.706, 0.735, 0.756, 0.774]; # voltage across diode measured using AM
        Id_AM = []; 
        for i in range(0, len(Vd_AM), 1):
            Id_AM.append(Vr_AM[i] / Rd)

        # make a fit to the data using the diode equation
        pars_AM = diode_fit(Id_AM, Vd_AM, T); 

        # generate residual data based on fit
        Vd_AM_fit = []
        for i in range(0, len(Id_AM), 1):
            Vd_AM_fit.append( diode_voltage(Id_AM[i], pars_AM[0], pars_AM[1], T) )

        # Make a plot of the standard measurement with its fit
        args = Plotting.plot_arg_multiple()

        hv_data = []; 
        hv_data.append([Id_std, Vd_std])
        hv_data.append([Id_std, Vd_std_fit])

        args.loud = True
        args.crv_lab_list = ["Std.", "Fit"]
        args.mrk_list = [ Plotting.labs_pts[0], Plotting.labs_lins[1] ]
        args.x_label = 'Current / mA'
        args.y_label = 'Voltage / V'
        args.fig_name = "Diode_Std_Meas_Rd_10"
        args.plt_range = [0, 111, 0, 0.8]

        Plotting.plot_multiple_curves(hv_data, args)

        hv_data = []; 
        hv_data.append([Id_AM, Vd_AM])
        hv_data.append([Id_AM, Vd_AM_fit])

        args.crv_lab_list = ["AM", "Fit"]
        args.fig_name = "Diode_AM_Meas_Rd_10"
        
        Plotting.plot_multiple_curves(hv_data, args)

        # plot the combined data
        #args = Plotting.plot_arg_multiple()

        #hv_data = []; 
        #hv_data.append([Id_std, Vd_std])
        #hv_data.append([Id_AM, Vd_AM])

        #args.loud = False
        #args.crv_lab_list = ["Std.", "AM"]
        #args.mrk_list = [ Plotting.labs[0], Plotting.labs[1] ]
        #args.x_label = 'Current / mA'
        #args.y_label = 'Voltage / V'
        #args.fig_name = "Diode_Meas_Rd_10"
        #args.plt_range = [0, 111, 0, 0.8]

        #Plotting.plot_multiple_curves(hv_data, args)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def AM_Diode_Meas_Compar_2():

    # Plot the measured diode characteristic data
    # data taken from a standard set-up and an AM based set-up
    # R. Sheehan 8 - 7 - 2021

    FUNC_NAME = ".AM_Diode_Meas_Compar()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_Diode_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        # the data obtained manually
        Rd = 0.01; # impedance of resistor used to determine diode current
        Vr_std = [0, 0, 0, 0, 0, 0.004, 0.0256, 0.0727, 0.1306, 0.1983, 0.269, 
                  0.35, 0.427, 0.508, 0.588, 0.678, 0.76, 0.845, 0.929, 1.019, 1.103]; # voltage across diode resistor measured using standard set up
        Vd_std = [0, 0.0922, 0.1895, 0.295, 0.392, 0.487, 0.561, 0.615, 0.649, 0.675, 
                  0.694, 0.708, 0.726, 0.737, 0.747, 0.755, 0.765, 0.772, 0.779, 0.786, 0.791]; # voltage across diode measured using standard set up
        Id_std = []; # current going into diode measured using standard set up
        for i in range(0, len(Vr_std), 1):
            Id_std.append(Vr_std[i] / Rd)

        fname = "AM_FR101_Swp_%(v1)d_Rd_10.txt"

        #diode_data = numpy.array([])
        for j in range(1, 4, 1):
            file = fname%{"v1":j}
            print(file)
            #data = numpy.loadtxt(file, delimiter = '\t', unpack = True); 
            diode_data = numpy.loadtxt(file, delimiter = '\t', unpack = True); 
            #if j == 1:
            #    diode_data = data
            #else:
            #    diode_data = numpy.append(diode_data, data, 1)

            # sort the data
            #diode_data[1], diode_data[0] = Common.sort_two_col(diode_data[1], diode_data[0])

            # make a fit to the data using the diode equation
            T = 20; 
            pars_std = diode_fit(diode_data[0], diode_data[1], T); 

            # generate residual data based on fit
            Vd_fit = []
            for k in range(0, len(diode_data[0]), 1):
                Vd_fit.append( diode_voltage(diode_data[0][k], pars_std[0], pars_std[1], T) )

            # Make a plot of the data
            args = Plotting.plot_arg_multiple()

            hv_data = []; 
            hv_data.append([diode_data[0], diode_data[1]])
            hv_data.append([diode_data[0], Vd_fit])

            args.loud = True
            args.crv_lab_list = ["Data", "Fit"]
            args.mrk_list = [ Plotting.labs_pts[0], Plotting.labs_lins[1] ]
            args.x_label = 'Current / mA'
            args.y_label = 'Voltage / V'
            args.fig_name = file.replace(".txt","")
            args.plt_range = [0, 130, 0, 0.9]

            Plotting.plot_multiple_curves(hv_data, args)

            hv_data = []; 
            hv_data.append([diode_data[0], diode_data[1]])
            hv_data.append([Id_std, Vd_std])

            args.crv_lab_list = ["AM", "Std"]
            args.mrk_list = [ Plotting.labs_pts[0], Plotting.labs_pts[1] ]
            args.fig_name = file.replace(".txt","") + "_vs_Man_Meas"

            Plotting.plot_multiple_curves(hv_data, args)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def diode_voltage(x, eta, eye0, T):
    # ideal diode equation inverted for voltage with Ohm's law contribution
    # across diode included, see Tyndall Notebook 2353, page 100
    # (k_{B} / q) = 8.61733e-5 [J / C K]
    # series resistance needs to have negative sign for some reason
    # what does eye0 represent? Bias saturation current

    # For this function to work you need to use np.log, not math.log!!!

    # need to define temperature as a global variable so that it gets assigned when function is called
    T_term = 8.61733e-5*Common.convert_C_K(T) # at T = 25 C T_term = 0.0256926 [J/C]
    
    return ( eta*T_term*numpy.log( 1.0 + (x/eye0) ) )

def diode_fit(hor_data, vert_data, T):
    # fit the diode voltage equation to the data
    # it is assumed that hor_data is input in units of mA and vert_data in units of V
    # Temperature T is input in units of deg C
    # T is converted to units of K inside function diode_voltage
    # I_{0} is computed in units of mA, printed in units of uA
    # eta is dimensionless

    from scipy.optimize import curve_fit

    params = ['eta', 'I_{0}']

    # lambda function needed to include temperature dependence in fit calculations
    # https://docs.python.org/2/tutorial/controlflow.html#lambda-expressions

    popt, pcov = curve_fit( lambda x, eta, eye0: diode_voltage(x, eta, eye0, T), hor_data, vert_data )

    #print("Fit parameters =",popt)
    #print("Fit covariance =",pcov)
    print("eta =", popt[0], " +/- ", math.sqrt(abs(pcov[0][0])) ) # dimensionless
    print("I_{0} =", 1000*popt[1], " +/- ", 1000*math.sqrt(abs(pcov[1][1])), "uA" ) # computed in units of mA, express in uA fo convenience

    #for i in range(0, len(params), 1):
    #    print(params[i]," =",popt[i]," +/-",math.sqrt(abs(pcov[i][i])))

    print(" ")

    return popt

def AM_BJT_Meas_Compar():

    # Plot the measured BJT characteristic data
    # data taken from a standard set-up and an AM based set-up
    # R. Sheehan 8 - 7 - 2021

    FUNC_NAME = ".AM_BJT_Meas_Compar()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/Users/" + USER +  "/Teaching/PY2108/Data/AM_BJT_Test/"

        os.chdir(DATA_HOME)

        print(os.getcwd())

        Ic15=[0, 0, 0, 0, 2.8, 12.57142857, 23.04285714, 31.41428571, 34.91428571, 
              39.8, 41.88571429, 42.58571429, 46.08571429, 46.08571429, 50.28571429, 52.35714286] # Measured collector current for Vbset = 1.5 V
        Ib15=[1.075, 1.124, 0.929, 1.075, 0.879, 0.684, 0.586, 0.489, 0.44, 0.342, 
              0.342, 0.489, 0.293, 0.489, 0.489, 0.293] # Measured base current for Vbset = 1.5 V
        Vce15=[0, 0, 0, 0, 0.0244, 0.0782, 0.1271, 0.2151, 0.347, 0.5083, 0.6794, 
               0.8407, 1.0068, 1.1681, 1.3196, 1.5152] # Measured collector-emitter voltage for Vbset = 1.5 V

        Ic16=[0, 0, 0, 0, 4.185714286, 16.75714286, 27.22857143, 37, 46.78571429, 
              55.85714286, 59.34285714, 63.54285714, 64.24285714, 65.62857143, 69.12857143, 71.22857143] # Measured collector current for Vbset = 1.6 V
        Ib16=[1.612, 1.661, 1.612, 1.612, 1.418, 1.125, 1.026, 0.928, 0.978, 
              0.782, 0.831, 0.782, 0.88, 0.929, 0.831, 0.978] # Measured base current for Vbset = 1.6 V
        Vce16=[0, 0, 0, 0, 0.0147, 0.0587, 0.0929, 0.1369, 0.1955, 0.2884, 
               0.435, 0.5865, 0.738, 0.8847, 1.0313, 1.173] # Measured collector-emitter voltage for Vbset = 1.6 V

        Ic17=[0, 0, 0, 0, 4.185714286, 16.75714286, 30.02857143, 41.9, 50.97142857, 
              60.74285714, 71.22857143, 76.81428571, 78.2, 81.68571429, 85.18571429, 83.8] # Measured collector current for Vbset = 1.7 V
        Ib17=[2.248, 2.248, 2.297, 2.248, 2.297, 2.151, 1.71, 1.662, 1.662, 
              1.613, 1.564, 1.368, 1.515, 1.417, 1.27, 1.417] # Measured base current for Vbset = 1.7 V
        Vce17=[0, 0, 0, 0, 0.0147, 0.0489, 0.0831, 0.1124, 0.1515, 0.1955, 
               0.259, 0.3519, 0.4643, 0.5914, 0.7136, 0.8895] # Measured collector-emitter voltage for Vbset = 1.7 V

        # plot the IV characteristic
        hv_data = []; labels = []; marks = []; 
        hv_data.append([Vce15, Ic15]); labels.append("$I_{b}\,=\,0.6$ mA"); marks.append(Plotting.labs_pts[0]); 
        hv_data.append([Vce16, Ic16]); labels.append("$I_{b}\,=\,1.1$ mA"); marks.append(Plotting.labs_pts[1]); 
        hv_data.append([Vce17, Ic17]); labels.append("$I_{b}\,=\,1.8$ mA"); marks.append(Plotting.labs_pts[2]); 

        # plot the data
        args = Plotting.plot_arg_multiple()

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Collector-Emitter Voltage / V'
        args.y_label = 'Collector Current / mA'
        args.fig_name = "AM_BJT_IV"
        args.plt_range = [0, 1.6, 0, 90]
        args.plt_title = "$R_{b}\,=\,100\,\Omega,\,R_{c}\,=\,7\,\Omega$"

        #Plotting.plot_multiple_curves(hv_data, args)

        # plot the gain characteristic
        hv_data = []; labels = []; marks = []; 
        hv_data.append([Ib15, Ic15]); labels.append("$I_{b}\,=\,0.6$ mA"); marks.append(Plotting.labs_pts[0]); 
        hv_data.append([Ib16, Ic16]); labels.append("$I_{b}\,=\,1.1$ mA"); marks.append(Plotting.labs_pts[1]); 
        hv_data.append([Ib17, Ic17]); labels.append("$I_{b}\,=\,1.8$ mA"); marks.append(Plotting.labs_pts[2]); 

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.x_label = 'Base Current / mA'
        args.y_label = 'Collector Current / mA'
        args.fig_name = "AM_BJT_Gain_1"
        args.plt_range = [0, 2.5, 0, 90]
        args.plt_title = "$R_{b}\,=\,100\,\Omega,\,R_{c}\,=\,7\,\Omega$"

        #Plotting.plot_multiple_curves(hv_data, args)

        args.fig_name = "AM_BJT_Gain_Fit_1"
        Plotting.plot_multiple_linear_fit_curves(hv_data, args)

        # plot the gain characteristic
        hv_data = []; labels = []; marks = []; 
        hv_data.append([Ic15, Ib15]); labels.append("$I_{b}\,=\,0.6$ mA"); marks.append(Plotting.labs_pts[0]); 
        hv_data.append([Ic16, Ib16]); labels.append("$I_{b}\,=\,1.1$ mA"); marks.append(Plotting.labs_pts[1]); 
        hv_data.append([Ic17, Ib17]); labels.append("$I_{b}\,=\,1.8$ mA"); marks.append(Plotting.labs_pts[2]); 

        args.loud = True
        args.crv_lab_list = labels
        args.mrk_list = marks
        args.y_label = 'Base Current / mA'
        args.x_label = 'Collector Current / mA'
        args.fig_name = "AM_BJT_Gain_2"
        args.plt_range = [0, 90, 0, 2.5]
        args.plt_title = "$R_{b}\,=\,100\,\Omega,\,R_{c}\,=\,7\,\Omega$"

        #Plotting.plot_multiple_curves(hv_data, args)

        args.fig_name = "AM_BJT_Gain_Fit_2"
        Plotting.plot_multiple_linear_fit_curves(hv_data, args)
        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)