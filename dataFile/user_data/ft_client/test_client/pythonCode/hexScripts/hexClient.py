#/usr/bin/python
"""
Map Prime Hexagon calculation

by Julian Gutierrez
NUCAR High Performance Computing
2017

"""
import sys
import os
import argparse
import itertools
import functions
# import configparser # currently hnot installed
from time import time

import hexWrapper
from hexConnector import runConnection
#import functions

if __name__ == "__main__":

    print ("Reading Configuration File")
    
    #settings = configparser.ConfigParser()
    #settings._interpolation = configparser.ExtendedInterpolation()
    #settings.read('config.ini')#

    # Config variables
    run_dec  = 11#eval(settings.get('DIRCONFIG', 'RUN_DECIMALS'))   # Number of figures represented by each file line
    
    print ("Parsing Arguments")
    
    parser = argparse.ArgumentParser(description = 'Prime Hexagon: Mapping Function',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--outputDir', default = "./output",	 type=str,		 help='Directory where finished files will be moved to.')
    parser.add_argument('--gpuNum', default = 0, 		 type=int,		 help='GPU number to calculate on. Default is 0.'

    args = parser.parse_args()

    # Check which is the latest directory/file created and look for the last checkpoint stored to start from there.
    print ("Checking Directory Structure")

    if not os.path.exists("./temp"):
	os.makedirs("./temp")

    if not os.path.exists(args.outputDir):
	os.makedirs(args.outputDir)

    def generateFile(outputDirectory, lineIncrement, fileName):
	color = 0

	sys.stdout.write( "Writing to file, value starting at: %s\n" % str(fileName))
	if os.path.exists(os.path.join("./temp",fileName + ".txt~")):
	    os.remove(os.path.join("./temp",fileName + ".txt~"))
        f = open(os.path.join("./temp", fileName + ".txt~"), "a+")
        f.write(str(color)) + '\n')
        f.close()
	for lineNum in range(1,10**2+1):
	    sys.stdout.flush()
	    output = hexWrapper.runHex(str(fileName)+str(lineNum-1).zfill(2)+''.zfill(lineIncrement),
	        str(color),
		str(fileName)+str(lineNum).zfill(2)+''.zfill(lineIncrement))

	    print("New color: ", output)
	    color = output

	    f = open(os.path.join("./temp", fileName + ".txt~"), "a+")
	    f.write("%s" % str(output) + '\n')
	    f.close()
	
	print("moving " + os.path.join("./temp", fileName + ".txt~") + " to " + os.path.join(outputDirectory, fileName + ".txt~"))
	# rename temporary file to final filename once finished
	os.rename(os.path.join("./temp", fileName + ".txt~"), os.path.join(outputDirectory, fileName + ".txt~"))

	return { "success": True, "message": "File " + str(fileName) + ".txt~ created. Saved to directory: " + outputDirectory }


    # call http connector to run hex program
    runConnection(lambda number: generateFile(args.outputDir, run_dec, number, args.gpuNum))
	
