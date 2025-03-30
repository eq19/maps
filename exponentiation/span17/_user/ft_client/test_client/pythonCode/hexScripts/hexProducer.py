#/usr/bin/python
"""
Map Prime Hexagon calculation

by Julian Gutierrez, Sam Smucny
NUCAR High Performance Computing
2017

Summary:
Generates files of 100 lines each that specify the colors of integers at intervals of 100 billion (entire file then spans 10 trillion).
The files generated always start with 0, so they need to be shifted before they are sorted into the finalized data store. 

Instructions:
python hexProducer.py [--outputDir {string}] [--gpu {integer}] [--start {integer}] [--finish {integer}]

All arguments are optional and have default values.
The program produces an output of the colors generated at each line and the range that the color was generated for.

"""
import sys
import os
import argparse
import itertools
import functions
# import configparser # currently hnot installed
from time import time

import hexWrapper
#import functions

if __name__ == "__main__":

    print ("Reading Configuration File")
    
    #settings = configparser.ConfigParser()
    #settings._interpolation = configparser.ExtendedInterpolation()
    #settings.read('config.ini')#

    # Config variables
    path_dec = 7#eval(settings.get('DIRCONFIG', 'PATH_DECIMALS'))  # Number of figures in path name
    file_dec = 3#eval(settings.get('DIRCONFIG', 'FILE_DECIMALS'))  # Number of figures in file name
    run_dec  = 11#eval(settings.get('DIRCONFIG', 'RUN_DECIMALS'))   # Number of figures represented by each file line
    goal_dec = 21#eval(settings.get('DIRCONFIG', 'GOAL_DECIMALS'))  # Maximum number of figures in search space
    
    #write_type = settings.get('FILEOUT', 'TYPE')
   
    print ("Parsing Arguments")
    
    parser = argparse.ArgumentParser(description = 'Prime Hexagon: Mapping Function',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--outputDir', default = "./output",	 type=str,		 help='Directory where finished files will be moved to.')
    parser.add_argument('--start',      default = 0,             type=int,               help='Number to start calculating from.')
    parser.add_argument('--finish',     default = 10**goal_dec,  type=int,               help='Number to calculate too.')
    parser.add_argument('--gpu', 	default = 0,	         type=int,		 help='gpu Num to utilize (default 0)')
   # parser.add_argument('--offset',     default = 0,		 type=int,	 	 help='Value to offset file generation at. Only one process should be running with a given offset at a time.')
    #parser.add_argument('--inc',	default = 1,		 type=int,		 help='Value by which to increment file names')

    args = parser.parse_args()

    # Check which is the latest directory/file created and look for the last checkpoint stored to start from there.
    print ("Checking Directory Structure")
    
    # create directory to store output if it does not already exist
    #if not os.path.exists(args.dir):
        #os.makedirs(args.dir)

    if not os.path.exists("./temp"):
	os.makedirs("./temp")

    if not os.path.exists(args.outputDir):
	os.makedirs(args.outputDir)

    # Marker in case startingpoint is different than 0
    mark = ''
    if args.start != 0:
	mark = '~'
    
    # Marker to indicate if calculating the first element
    first = 1

    # Each filename is generated from the start and end numbers divided by the increment for each file (default is 10 trillion 10^13)
    for path in range(int(args.start/(10**(run_dec+2))),int(args.finish/(10**(run_dec+2)))):

	# take loop variable and convert it into a continous string representing 
	# the number to start processing at with the {goal_dec-path_dec} least significant digits truncated
	currentPath = str(path).zfill(path_dec+file_dec)

	# start color for first number in file at 0 since it is currently unknown
	color = 0
	flag = "~"

	sys.stdout.write( "Writing to file, value starting at: %s\n" % currentPath)
	if os.path.exists(os.path.join("./temp",currentPath + ".txt" + flag)):
	    os.remove(os.path.join("./temp",currentPath + ".txt" + flag))
	if os.path.exists(os.path.join(args.outputDir,currentPath + ".txt")):
	    break # if the file already has been generated then this program is finished
	for lineNum in range(10**2+1):
	    #sys.stdout.write( "Writing to file, value for: %s\n" % (str(lineNum).zfill(file_dec)))
	    sys.stdout.flush()
	    if lineNum == 0:
		color = 0
	    elif lineNum == 100:
		color = hexWrapper.runHex(str(path)+str(99)+''.zfill(run_dec),
		    str(color),
		    str(path+1)+'00'+''.zfill(run_dec), args.gpu)
	    else:
		color = hexWrapper.runHex(str(path)+str(lineNum-1).zfill(2)+''.zfill(run_dec),
		    str(color),
		    str(path)+str(lineNum).zfill(2)+''.zfill(run_dec), args.gpu)

	    print("Line: ", lineNum, "Color: ", color)

	    f = open(os.path.join("./temp", currentPath + ".txt" + flag), "a+")
	    f.write("%s" % str(color) + '\n')
	    f.close()
	
	print("moving " + os.path.join("./temp", currentPath + ".txt" + flag) + " to " + os.path.join(args.outputDir, currentPath + ".txt"))
	# rename temporary file to final filename once finished
	os.rename(os.path.join("./temp", currentPath + ".txt" + flag), os.path.join(args.outputDir, currentPath + ".txt"))
