import sys
import os 

# add path to our file
#sys.path.append('c:/Users/Robert/Programming/Python/Common/')
#sys.path.append('c:/Users/Robert/Programming/Python/Plotting/')

import PY3108
import PY2108

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)

    #PY3108.Plot_CE_Amp()

    #PY3108.OpAmpComparison()

    PY2108.LRC_FR_Plots()