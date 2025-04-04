#/usr/bin/python
"""
Map Prime Hexagon calculation

by Julian Gutierrez
by Sam Smucny
NUCAR High Performance Computing
2017

"""
import sys
import os
import argparse
import itertools
import functions
# import configparser # currently hnot installed

import hexWrapper

def generateFile(outputDirectory, lineIncrement, fileName, gpuNum):
	if not os.path.exists("./temp"):
	    os.makedirs("./temp")

	if not os.path.exists(outputDirectory):
	    os.makedirs(outputDirectory)

	color = 0

	sys.stdout.write( "Writing to file, value starting at: %s\n" % str(fileName))
	if os.path.exists(os.path.join("./temp",fileName + ".txt~")):
	    os.remove(os.path.join("./temp",fileName + ".txt~"))
	f = open(os.path.join("./temp", fileName + ".txt~"), "a+")
	f.write(str(color)) + '\n')
	f.close()
	for lineNum in range(10**2+1):
	    sys.stdout.flush()
	    output = hexWrapper.runHex(str(fileName)+str(lineNum-1).zfill(2)+''.zfill(lineIncrement),
		str(color),
		str(fileName)+str(lineNum).zfill(2)+''.zfill(lineIncrement), gpuNum)

	    print("Line:", lineNum, "Color:", output)
	    color = output

	    f = open(os.path.join("./temp", fileName + ".txt~"), "a+")
	    f.write("%s" % str(output) + '\n')

	# generate the 101th line
        fsys.stdout.flush()
        output = hexWrapper.runHex(str(fileName)+str(99)+''.zfill(lineIncrement),
	    str(color),
	    str(fileName+1)+'00'+''.zfill(lineIncrement), gpuNum)
        
        print("Line:", 100, "Color:", output)
        color = output

        f = open(os.path.join("./temp", fileName + ".txt~"), "a+")
        f.write("%s" % str(output) + '\n')
        f.close()

	print("moving " + os.path.join("./temp", fileName + ".txt~") + " to " + os.path.join(outputDirectory, fileName + ".txt"))
	# rename temporary file to final filename once finished
	os.rename(os.path.join("./temp", fileName + ".txt~"), os.path.join(outputDirectory, fileName + ".txt"))

	return { "success": True, "message": "File " + str(fileName) + ".txt created. Saved to directory: " + outputDirectory }
