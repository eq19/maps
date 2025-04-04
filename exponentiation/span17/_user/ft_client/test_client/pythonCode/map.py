#!/usr/bin/python
"""
Map Prime Hexagon calculation

by Julian Gutierrez
NUCAR High Performance Computing
2017

"""
import sys
import os
import argparse
#import configparser
from time import time

import hexScripts.hexWrapper
import hexScripts.functions

if __name__ == "__main__":

    #print ("Reading Configuration File")
    
    #settings = configparser.ConfigParser()
    #settings._interpolation = configparser.ExtendedInterpolation()
    #settings.read('config.ini')#

    # Config variables
    path_dec = 5#eval(settings.get('DIRCONFIG', 'PATH_DECIMALS'))
    file_dec = 5#eval(settings.get('DIRCONFIG', 'FILE_DECIMALS'))
    run_dec  = 11#eval(settings.get('DIRCONFIG', 'RUN_DECIMALS'))
    goal_dec = 21#eval(settings.get('DIRCONFIG', 'GOAL_DECIMALS'))
    
    #write_type = settings.get('FILEOUT', 'TYPE')
   
    print ("Parsing Arguments")
    
    parser = argparse.ArgumentParser(description = 'Prime Hexagon: Mapping Function',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dir',        default = "./",          type=str,               help='Directory where the results will be stored.')
    parser.add_argument('--start',      default = 0,             type=int,               help='Number to start calculating from.')
    parser.add_argument('--finish',     default = 10**goal_dec,  type=int,               help='Number to calculate too.')

    args = parser.parse_args()

    # Check which is the latest directory/file created and look for the last checkpoint stored to start from there.
    print ("Checking Directory Structure")
    
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
        
    # Marker in case startingpoint is different than 0
    mark = ''
    if args.start != 0:
        mark = '!'
    
    # Marker to indicate if calculating the first element
    first = 1
    print(args.finish)
    # TODO: CHECK THIS STATEMENT!
    for path in range (int((args.start/(10**(goal_dec-path_dec)))),int(args.finish/(10**(goal_dec-path_dec)))):
        currentPath = str(path).zfill(path_dec)
        currentDir  = args.dir+'/'+currentPath[:1]+'/'+currentPath[1:3]+'/'
        currentFile = currentPath[3:path_dec]
        color = 0
        
        if not os.path.exists(currentDir):
            os.makedirs(currentDir)
            print ("Making Dir: %s" % currentDir)
        
        if not os.path.exists(currentDir+currentFile):
            size = 0
        else:
            print ("File %s exists, checking last entry." % (currentDir+currentFile))
            size,color = hexScripts.functions.fileLen(currentDir+currentFile)
        
        if size == 10**run_dec:
            # This path file is done, lets move on to the next
            continue
            
        for run in range(size,10**file_dec):
            sys.stdout.write( "Writing to file, value for: %s" % (currentDir+currentFile+'-'+str(run).zfill(file_dec)))
            sys.stdout.flush()
            
            if run == 0:
                if first == 1:
                    first = 0
                    if mark == '!':
                        output = "!0"
                    else:    
                        output = "0"
                else:
                    output = hexScripts.hexWrapper.runHex(str(path-1)+str(10**file_dec-1)+''.zfill(run_dec),
                            str(color),
                            str(path)+str(run).zfill(file_dec)+''.zfill(run_dec))
            else:
                output = hexScripts.hexWrapper.runHex(str(path)+str(run-1).zfill(file_dec)+''.zfill(run_dec),
                            str(color),
                            str(path)+str(run).zfill(file_dec)+''.zfill(run_dec))
            print (" - Done")
            
            # Add mark in case the startpoint is not 0
            output = mark + str(output) + '\n'
            
            f = open(currentDir+currentFile,"a+")
            f.write("%s" % output)
            f.close()
            color = output           
