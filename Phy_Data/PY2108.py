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

def AM_Diode_Meas_Compar():

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