
# Prime Hexagon calculation for numbers close to pi
# by Daniel Goldstein
# NUCAR High Performance Computing
# March 30 2017

import sys
import csv

from sys import argv
from decimal import *
from datetime import datetime
from pythonCode import *


script, output = argv

# Number parameters for the range of numbers to be tested
lower_bound = 0#Decimal( str(input("What is the lower bound? ")) )
upper_bound = 169#Decimal( str(input("What is the upper bound? ")) )
range_slice = 1#Decimal( str(input("How fine a slice?        ")) )
precision   = 15#int(     input("How many dec places?     ") )
power_limit = 1#int(     input("How many powers?         ") )

# Start the time
start_time = datetime.now()
# keep track of the hexpinum objects that have finished the iteration
finished = []

# Begin looping through the range, starting with lower_bound
current = utilities.Hexnum(lower_bound, power_limit, precision)

while (current.val <= upper_bound):

    for num in current.powers:

        #figure out which file to use
        file_index = utilities.find_plist(num)
        if file_index is not None:
            pfile = open(utilities.plists[file_index], 'r')
            #determine spin color
            mult = utilities.get_spin_nums(num, pfile)
            pfile.close()
        else:
            mult = (5, 5)

        #get the color that corresponds to that multiplication
        color = utilities.spin.get(mult, None) + "_" + str(num % 6)
        print(num,mult,color)
        current.add_color(color) #add on the power and its associated color
        current.set_roll_double() # set_roll_double(current)
        #see if there were any doubles and set the roll_double field
        if(current.roll_double or None in current.colors):
            break


    #all done, add the finished Hexnum onto the list and move on
    finished.append(current)

    #reset the current to the next Hexnum
    current = utilities.Hexnum(current.val + range_slice, power_limit, precision)

# end of while loop

# write contents to file/process etc.
output_path = 'user_data/ft_client/test_client/results/{}'.format(output)
results = open(output_path, 'w')
results.truncate()

# write at what power a number rolls a double
for num in finished:
    if None in num.colors:
        results.write("%s %s Limit Reached\n" % (num.val, ' '.join([str(c) for c in num.colors])))
    else:
        results.write("%s %s\n" % (num.val, ' '.join([str(c) for c in num.colors])))

results.close()

# Print how long it took
#print(datetime.now() - start_time)

if __name__ == '__main__':
    #program, *args = sys.argv
    #if len(args) == 0:
        #print(f"Usage: {program} <path/to/Main.class>")
        #print(f"ERROR: no path to Main.class was provided")
        #exit(1)
    #file_path, *args = args
    clazz = jello.parse_class_file('user_data/ft_client/test_client/Main.class')
    [main] = jello.find_methods_by_name(clazz, b'main')
    [code] = jello.find_attributes_by_name(clazz, main['attributes'], b'Code')
    code_attrib = jello.parse_code_info(code['info'])
    jello.execute_code(clazz, code_attrib['code'])
